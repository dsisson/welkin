import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.teladoc.base_page import BaseWrapperPageObject

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
            'Primary Care': ['Expert Care', 'Primary Care'],
            'Specialty & Wellness Care': ['Expert Care', 'Specialty & Wellness Care'],
            'Adults': ['For Individuals', 'Adults'],
            '(Hospitals) Virtual Care Platform': ['For Organizations', '(Hospitals) Virtual Care Platform'],
            '(Health Plans) Mental Health': ['For Organizations', '(Health Plans) Mental Health'],
            '(Employers) Chronic Care': ['For Organizations', '(Employers) Chronic Care']
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.teladochealth.com/'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='/']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "header a[href='/']"),
                        'po': 'teladoc home page',
                        'target': '/'
                    }
                },
            },
            'Expert Care': {
                'sel_stage1': (By.XPATH, "//header//button[text()='Expert Care']"),
                'stage2': {
                    'Primary Care': {
                        'sel': (By.XPATH, "//header//a[text()='Primary Care']"),
                        'po': 'teladoc expert primary care page',
                        'target': '/expert-care/primary-care/'
                    },
                    'Specialty & Wellness Care': {
                        'sel': (By.XPATH, "//header//a[text()='Specialty & Wellness Care']"),
                        'po': 'teladoc expert speciality care page',
                        'target': '/expert-care/specialty-wellness/'
                    },
                },
            },
            'For Individuals': {
                'sel_stage1': (By.XPATH, "//header//button[text()='For Individuals']"),
                'stage2': {
                    'Adults': {
                        'sel': (By.XPATH, "//header//a[text()='Adults']"),
                        'po': 'teladoc care for adults page',
                        'target': '/individuals/adults/'
                    },
                },
            },
            'For Organizations': {
                'sel_stage1': (By.XPATH, "//header//button[text()='For Organizations']"),
                'stage2': {
                    '(Hospitals) Virtual Care Platform': {
                        'sel': (By.XPATH, "//a[contains(@href, "
                                          "'/organizations/hospitals-health-systems/virtual-care-platform/')]"),
                        'po': 'teladoc orgs hospital virtual care platform page',
                        'target': '/organizations/hospitals-health-systems/virtual-care-platform/'
                    },
                    '(Health Plans) Mental Health': {
                        'sel': (By.XPATH, "//a[contains(@href, "
                                          "'/organizations/health-plans/mental-health/')]"),
                        'po': 'teladoc orgs health plans mental health page',
                        'target': '/organizations/health-plans/mental-health/'
                    },
                    '(Employers) Chronic Care': {
                        'sel': (By.XPATH, "//a[contains(@href, "
                                          "'/organizations/employers/chronic-care-management/')]"),
                        'po': 'teladoc orgs employers chronic care page',
                        'target': '/organizations/employers/chronic-care-management/'
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
