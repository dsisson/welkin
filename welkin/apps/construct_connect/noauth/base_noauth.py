import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.construct_connect.base_page import BaseWrapperPageObject

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
            'Find More Bids': ['Solutions', 'Find More Bids'],
            'Quickly Create & Send Bid Invites': ['Solutions', 'Quickly Create & Send Bid Invites'],
            'Bid Center': ['Products', 'Bid Center'],
            'Grab the Survival Kit': ['Resources', 'Grab the Survival Kit'],
            'Careers': ['About', 'Careers'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.constructconnect.com'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, f"header a[href='{base}']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, f"header a[href='{base}']"),
                        'po': 'construct home page',
                        'target': '/'
                    }
                },
            },
            'Solutions': {
                'sel_stage1': (By.XPATH, "//header//a[text()='Solutions']"),
                'stage2': {
                    'Find More Bids': {
                        'sel': (By.XPATH, "//header//a[text()='Find More Bids']"),
                        'po': 'construct subcontractors page',
                        'target': '/subcontractors'
                    },
                    'Quickly Create & Send Bid Invites': {
                        'sel': (By.XPATH, "//header//a[text()='Quickly Create & Send Bid Invites']"),
                        'po': 'construct general contractors page',
                        'target': '/general-contractors'
                    },
                },
            },
            'Products': {
                'sel_stage1': (By.XPATH, "//header//a[text()='Products']"),
                'stage2': {
                    'Bid Center': {
                        'sel': (By.XPATH, "//header//a[text()='Bid Center']"),
                        'po': 'construct bid center page',
                        'target': '/bid-center'
                    },
                },
            },
            'Resources': {
                'sel_stage1': (By.XPATH, "//header//a[text()='Resources']"),
                'stage2': {
                    'Grab the Survival Kit': {
                        'sel': (By.XPATH, "//header//a[text()='Grab the Survival Kit']"),
                        'po': 'construct survival kit page',
                        'target': '/construction-estimating-survival-kit'
                    },
                },
            },
            'About': {
                'sel_stage1': (By.XPATH, "//header//a[text()='About']"),
                'stage2': {
                    'Careers': {
                        'sel': (By.XPATH, "//header//a[text()='Careers']"),
                        'po': 'construct careers page',
                        'target': '/careers'
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
                                                  actions={'unhover': (0, -60)})
        return next_page
