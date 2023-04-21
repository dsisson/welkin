import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.allergan.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page as scroll_up

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
            'A-DL': {
                'sel': '//a[@href="/"]',
                'po': 'allergan home page',
                'target': '/'
            },
            'Allē': {
                'sel': '//a[@href="/alle"]',
                'po': 'allergan alle page',
                'target': '/alle'
            },
            'Careers': {
                'sel': '//a[@href="/careers"]',
                'po': 'allergan careers page',
                'target': '/careers'
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
