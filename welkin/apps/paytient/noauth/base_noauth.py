import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.paytient.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def generate_nav_path(self, target):
        """
            Convert the desired `target` str into a list of two str nav targets,
            where the first is an activator for a dynamic sub-menu, and the
            second is the actual desired page.

            :param target:
            :return: list of stage1 and stage 2 nav targets
        """
        map_destination_to_path = {
            'Home': ['Home', 'Home'],
            'Employers': ['For Partners', 'Employers'],
            'Insurers': ['For Partners', 'Insurers'],
            'Start Here': ['For Paytients', 'Start Here'],
            'What is an HPA?': ['For Paytients', 'What is an HPA?'],
            'Blog': ['Resources', 'Blog'],
            'Guides': ['Resources', 'Guides'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.paytient.com'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "div.navbar_container a[href='/']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "div.navbar_container a[href='/']"),
                        'po': 'paytient home page',
                        'target': '/'
                    }
                },
            },
            'For Partners': {
                'sel_stage1': (By.XPATH, "//nav[@role='navigation']//div[text()='For Partners']"),
                'stage2': {
                    'Employers': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/employers']"),
                        'po': 'paytient employers page',
                        'target': '/employers'
                    },
                    'Insurers': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/insurers']"),
                        'po': 'paytient insurers page',
                        'target': '/insurers'
                    }
                }
            },
            'For Paytients': {
                'sel_stage1': (By.XPATH, "//nav[@role='navigation']//div[text()='For Paytients']"),
                'stage2': {
                    'Start Here': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/start']"),
                        'po': 'paytient start page',
                        'target': '/start'
                    },
                    'What is an HPA?': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/what-is-a-health-payment-account']"),
                        'po': 'paytient what is HPA page',
                        'target': '/what-is-a-health-payment-account'
                    },
                }
            },
            'Resources': {
                'sel_stage1': (By.XPATH, "//nav[@role='navigation']//div[text()='Resources']"),
                'stage2': {
                    'Blog': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/blog']"),
                        'po': 'paytient blog page',
                        'target': '/blog'
                    },
                    'Guides': {
                        'sel': (By.CSS_SELECTOR, "nav.navbar_dropdown-list a[href$='/guides']"),
                        'po': 'paytient guides page',
                        'target': '/guides'
                    },
                }
            },
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        # self.save_screenshot(event)

        # get the nav bar
        # nav = self.driver.find_element(By.TAG_NAME, "nav")

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # # however, this really needs a check that *something* happened here
        msg = 'hovered stage1 link'
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")
        self.set_event(msg, page_name=self.name)

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        logger.info(f"\nstage2 method: '{method}'")
        logger.info(f"\nstage2 selector: '{selector}'")
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")

        # logger.info(f"\nstage2_link:{stage2_link.get_attribute('innerHTML')}")

        event = f"clicked {target2} destination link"
        name = f"destination link {target2}"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['po']
        logger.info(f"\nstage2 po_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, 5)})
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            stage2_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)

        return next_page
