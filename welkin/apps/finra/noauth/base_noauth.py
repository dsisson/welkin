import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.finra.base_page import BaseWrapperPageObject

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def select_page_from_top_menu(self, target1):
        """
            This is a one-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param target1: str, identifier text for primary link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        target_links = {
            'About FINRA': {
                'sel': '//a[@href="/about"]',
                'po': 'finra about page',
                'target': '/about'
            },
            'Careers': {
                'sel': '//a[@href="/careers"]',
                'po': 'finra careers page',
                'target': '/careers'
            },
            'Media Center': {
                'sel': '//a[@href="/media-center"]',
                'po': 'finra media center page',
                'target': '/careers'
            },
            'For Firms': {
                'sel': '//a[@href="/member-firm-hub"]',
                'po': 'finra firm hub page',
                'target': '/member-firm-hub'
            },
        }

        # get the primary link element
        primary_link = self.driver.find_element(By.XPATH,
                                                target_links[target1]['sel'])

        # this is a one-stage link
        event1 = f"clicked {target1} primary link"
        name = f"primary link {target1}"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['po']

        # click the primary link, which will load the new page object
        next_page = self._click_and_load_new_page(primary_link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page

    def click_home_link(self):
        sel_home = '//a[@Title="Home"]'
        # get the primary link element
        link = self.driver.find_elements(By.XPATH, sel_home)[-1]

        event1 = f"clicked home page link"
        name = f"primary link home"

        # get the page object identifier for the target page
        po_selector = 'finra home page'

        # click the primary link, which will load the new page object
        next_page = self._click_and_load_new_page(link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
