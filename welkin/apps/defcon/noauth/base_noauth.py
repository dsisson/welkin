import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.defcon.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.defconai.com'

        target_links = {
            'Home': {
                'sel': (By.CSS_SELECTOR, "header nav a[href$='/']"),
                'po': 'defcon home page',
                'target': '/'
            },
            'MISSION': {
                'sel': (By.LINK_TEXT, "MISSION"),
                'po': 'defcon mission page',
                'target': '/mission'
            },
            'TEAM': {
                'sel': (By.LINK_TEXT, "TEAM"),
                'po': 'defcon team page',
                'target': '/team'
            },
            'CAPABILITIES': {
                'sel': (By.LINK_TEXT, "CAPABILITIES"),
                'po': 'defcon capabilities page',
                'target': '/capabilities'
            },
            'NEWS': {
                'sel': (By.LINK_TEXT, "NEWS"),
                'po': 'defcon news page',
                'target': '/news'
            },
            'CAREERS': {
                'sel': (By.LINK_TEXT, "CAREERS"),
                'po': 'defcon careers page',
                'target': '/careers'
            },
            'CONTACT US': {
                'sel': (By.LINK_TEXT, "CONTACT US"),
                'po': 'defcon contact us page',
                'target': '/contact-us'
            },

        }

        # get the nav bar
        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        self.save_screenshot(event)

        nav = self.driver.find_element(By.CSS_SELECTOR, 'nav#desktop-menu')

        # get the stage1 nav target element
        method, selector = target_links[destination]['sel']
        link = nav.find_element(method, selector)

        event = f"clicked {destination} destination link"
        name = f"{destination} destination link"

        # get the page object identifier for the target page
        po_selector = target_links[destination]['po']
        logger.info(f"\npo_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, 400)})
            self.set_event(event)
            # self.save_screenshot(event)
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            nav = self.driver.find_element(By.CSS_SELECTOR, 'nav#desktop-menu')
            method, selector = target_links[destination]['sel']
            link = nav.find_element(method, selector)

            next_page = self._click_and_load_new_page(link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)
            self.set_event(event)
        return next_page
