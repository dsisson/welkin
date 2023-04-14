import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.allstate.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page as scroll_up

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def switch_to_app(self):
        sel_switch_link = 'sign in'
        link = self.driver.find_element(By.LINK_TEXT, sel_switch_link)

        event = 'clicked sign-in link'
        name = 'sign-in link'

        # get the page object identifier for the target page
        po_selector = 'AIP login page'

        # click the primary link, which will load the new page object
        next_page = self._click_and_load_new_page(link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
