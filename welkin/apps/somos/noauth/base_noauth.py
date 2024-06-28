import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.somos.base_page import BaseWrapperPageObject
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
            'Fraud Mitigation & Data Integrity Solutions': ['Solutions', 'Fraud Mitigation & Data Integrity Solutions'],
            'Routing Optimization': ['Solutions', 'Routing Optimization'],
            'About': ['About', 'About'],
            'Our Team': ['About', 'Our Team'],
            'Insights': ['Insights', 'Insights'],
            'Events': ['Events', 'Events'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.somos.com'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[title='Home']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "header a[title='Home']"),
                        'po': 'somos home page',
                        'target': '/'
                    }
                },
            },
            'Solutions': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/about/who-we-serve']"),
                'stage2': {
                    'Fraud Mitigation & Data Integrity Solutions': {
                        'sel': (By.CSS_SELECTOR, "ul.main-nav-subnav a[href='/our-solutions/fraud-mitigation-data-integrity-solutions']"),
                        'po': 'somos fraud mitigation page',
                        'target': '/our-solutions'
                    },
                    'Routing Optimization': {
                        'sel': (By.CSS_SELECTOR, "ul.main-nav-subnav a[href='/routing-optimization']"),
                        'po': 'somos routing data page',
                        'target': '/routing-optimization'
                    }
                }
            },
            'About': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/about']"),
                'stage2': {
                    'About': {
                        'sel': (By.CSS_SELECTOR, "header a[href='/about']"),
                        'po': 'somos about page',
                        'target': '/about'
                    },
                    'Our Team': {
                        'sel': (By.CSS_SELECTOR, "ul.main-nav-subnav a[href='/about/our-team']"),
                        'po': 'somos our team page',
                        'target': '/about/our-team'
                    }
                }
            },
            'Insights': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/insights']"),
                'stage2': {
                    'Insights': {
                        'sel': (By.CSS_SELECTOR, "header a[href='/insights']"),
                        'po': 'somos insights page',
                        'target': '/insights'
                    }
                }
            },
            'Events': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/events']"),
                'stage2': {
                    'Events': {
                        'sel': (By.CSS_SELECTOR, "header a[href='/events']"),
                        'po': 'somos events page',
                        'target': '/events'
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
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")

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
                                                      actions={'unhover': (0, 400)})
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            stage2_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)

        return next_page

    def select_option_from_cookie_modal(self, option):
        """
            Select an option from the cookie modal dialog.

            :param option: str, one of 'Accept' or 'Decline'
            :return: None
        """
        wait = WebDriverWait(self.driver, 5)
        # get the cookie modal dialog
        cookie_modal = None
        try:
            cookie_modal = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Privacy"]')))
            if option.lower() == 'cancel':
                control = self.driver.find_element(By.CSS_SELECTOR, 'button.onetrust-close-btn-handler')
            elif option.lower() == 'reject':
                control = self.driver.find_element(By.CSS_SELECTOR, 'button#onetrust-reject-all-handler')
            elif option.lower() == 'accept':
                control = self.driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
            else:
                msg = f"\nOption '{option}' not recognized, or no option provided, so taking no action"
                logger.info(msg)
                return

            element_name = f"cookie modal {option} button"

            msg = f"\nCookie modal option '{option}' selected; clicking that button"
            logger.info(msg)

            updated_page = self._click_and_load_new_page(control,
                                                         name=element_name,
                                                         po_selector=self.name,  # reload current page
                                                         change_url=False)
            return updated_page
        except TimeoutException:
            logger.info('\nno cookie modal')
