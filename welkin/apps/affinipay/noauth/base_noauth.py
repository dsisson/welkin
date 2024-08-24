import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.affinipay.base_page import BaseWrapperPageObject
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
            'About Us': ['Company', 'About Us'],
            'Newsroom': ['Company', 'Newsroom'],
            'Industry Perspective': ['Company', 'Industry Perspective'],
            'Careers': ['Careers', 'Careers'],
            'Contact Us': ['Contact Us', 'Contact Us'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.affinipay.com'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, ".main-nav a[aria-label='logo']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[aria-label='logo']"),
                        'po': 'affinipay home page',
                        'target': '/'
                    }
                },
            },
            'Company': {
                'sel_stage1': (By.CSS_SELECTOR, ".main-nav button#company-menu"),
                'stage2': {
                    'About Us': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[href='/company/about-us/']"),
                        'po': 'affinipay about us page',
                        'target': '/company/about-us/'
                    },
                    'Newsroom': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[href='/company/newsroom/']"),
                        'po': 'affinipay newsroom page',
                        'target': '/company/newsroom/'
                    },
                    'Industry Perspective': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[href='/industry-perspective/']"),
                        'po': 'affinipay industry perspective page',
                        'target': '/industry-perspective/'
                    }
                }
            },
            'Careers': {
                'sel_stage1': (By.CSS_SELECTOR, ".main-nav a[href='/careers/']"),
                'stage2': {
                    'Careers': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[href='/careers/']"),
                        'po': 'affinipay careers page',
                        'target': '/careers/'
                    },
                }
            },
            'Contact Us': {
                'sel_stage1': (By.CSS_SELECTOR, ".main-nav a[href='/contact-us/']"),
                'stage2': {
                    'Contact Us': {
                        'sel': (By.CSS_SELECTOR, ".main-nav a[href='/contact-us/']"),
                        'po': 'affinipay contact us page',
                        'target': '/contact-us/'
                    },
                }
            },
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        # self.save_screenshot(event)

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # click to trigger the submenu
        # self._click_element(stage1, name='dropdown trigger')

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
