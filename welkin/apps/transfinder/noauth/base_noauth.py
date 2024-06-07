import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.transfinder.base_page import BaseWrapperPageObject
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
            'Viewfinder': ['Solutions', 'Viewfinder'],
            'Tripfinder': ['Solutions', 'Tripfinder'],
            'Marketplace': ['Marketplace', 'Marketplace'],
            'Professional Services': ['Services', 'Professional Services'],
            'Case Studies': ['Resources', 'Case Studies'],
            'Company': ['About Us', 'Company'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.transfinder.com'

        # multiple templates, some of which don't support hover for submenus
        no_hover_templates = ['transfinder marketplace page']

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href='../']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href='../']"),
                        'po': 'transfinder home page',
                        'target': '/'
                    }
                },
            },
            'Solutions': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href$='/solutions/']"),
                'stage2': {
                    'Viewfinder': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href$='/solutions/Oversee_your_operation_anywhere_anytime']"),
                        'po': 'transfinder viewfinder page',
                        'target': '/solutions/Oversee_your_operation_anywhere_anytime'
                    },
                    'Tripfinder': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href$='/solutions/field_trip_management']"),
                        'po': 'transfinder tripfinder page',
                        'target': '/solutions/field_trip_management'
                    }
                }
            },
            'Marketplace': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href$='/marketplace/']"),
                'stage2': {
                    'Marketplace': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href$='/marketplace/']"),
                        'po': 'transfinder marketplace page',
                        'target': '/marketplace/'
                    },
                }
            },
            'Services': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href$='/services/']"),
                'stage2': {
                    'Professional Services': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href$='/services/professional-services']"),
                        'po': 'transfinder professional services page',
                        'target': '/services/professional-services'
                    },
                }
            },
            'Resources': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href$='/resources/']"),
                'stage2': {
                    'Case Studies': {
                        'sel': (By.CSS_SELECTOR, "div#header a[href$='/resources/case_studies.cfm']"),
                        'po': 'transfinder case studies page',
                        'target': '../resources/case_studies.cfm'
                    },
                }
            },
            'About Us': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header a[href$='/about-us/']"),
                'stage2': {
                    'Company': {
                        'sel': (By.CSS_SELECTOR, "div#header li.dropdown-submenu a[href$='/about-us/']"),
                        'po': 'transfinder about us page',
                        'target': '../about-us/'
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
        msg = None
        if self.name in no_hover_templates:
            msg = 'clicked stage1 link'
            self._click_element(stage1, name=destination)
            self.save_screenshot(f"click for target1")
        else:
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

    def close_popup(self):
        """
            Close a popup window that may appear on the page.
        """
        try:
            popup_closer = self.driver.find_element(By.CSS_SELECTOR, "div[id$='close']")
            self._click_element(popup_closer, name="close popup", msg="click 'x' to close")

        except NoSuchElementException:
            pass

        # reload the page object
        pageobject = self.load_pageobject(po_id=self.name)
        return pageobject
