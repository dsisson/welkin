import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.tome.base_page import BaseWrapperPageObject

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
            'AI in Tome': ['Product', 'AI in Tome'],
            'Integrations': ['Product', 'Integrations'],
            'Templates': ['Templates', 'Templates'],
            'Community': ['Community', 'Community'],
            'Pricing': ['Pricing', 'Pricing'],
            'Blog': ['Company', 'Blog'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://tome.app/'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "header a[href='/']"),
                        'po': 'tome home page',
                        'target': '/'
                    }
                },
            },
            'Product': {
                'sel_stage1': (By.XPATH, "//nav//button[text()='Product']"),
                'stage2': {
                    'AI in Tome': {
                        'sel': (By.CSS_SELECTOR, "nav a[href$='/ai']"),
                        'po': 'tome product ai page',
                        'target': '/ai'
                    },
                    'Integrations': {
                        'sel': (By.CSS_SELECTOR, "nav a[href$='/integrations']"),
                        'po': 'tome product integrations page',
                        'target': '/integrations'
                    },
                },
            },
            'Templates': {
                'sel_stage1': (By.XPATH, "//nav//li/a[text()='Templates']"),
                'stage2': {
                    'Templates': {
                        'sel': (By.XPATH, "//nav//a[text()='Templates']"),
                        'po': 'tome templates page',
                        'target': '/templates'
                    },
                },
            },
            'Community': {
                'sel_stage1': (By.XPATH, "//nav//li/a[text()='Community']"),
                'stage2': {
                    'Community': {
                        'sel': (By.XPATH, "//nav//a[text()='Community']"),
                        'po': 'tome community page',
                        'target': '/community'
                    },
                },
            },
            'Pricing': {
                'sel_stage1': (By.XPATH, "//nav//li/a[text()='Pricing']"),
                'stage2': {
                    'Pricing': {
                        'sel': (By.XPATH, "//nav//a[text()='Pricing']"),
                        'po': 'tome pricing page',
                        'target': '/pricing'
                    },
                },
            },
            'Company': {
                'sel_stage1': (By.XPATH, "//nav//button[text()='Company']"),
                'stage2': {
                    'Blog': {
                        'sel': (By.CSS_SELECTOR, "nav a[href$='/blog']"),
                        'po': 'tome blog page',
                        'target': '/blog'
                    },
                },
            },
        }

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # however, this really needs a check that *something* happened here
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")
        # self._goto_and_hover(stage2_link, name=target2)
        self.save_screenshot(f"hover for target2")

        logger.info(f"\nstage2_link:{stage2_link.get_attribute('innerHTML')}")

        event = f"clicked {target2} destination link"
        name = f"destination link {target2}"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['po']
        logger.info(f"\nstage2 po_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        next_page = self._click_and_load_new_page(stage2_link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True,
                                                  actions={'unhover': (0, 400)})
        return next_page
