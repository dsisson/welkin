import logging

from selenium.webdriver.common.by import By

from welkin.apps.examples.storyhealth.base_page import BaseWrapperPageObject
from welkin.framework import utils

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def select_page_from_top_menu(self, target):
        """
            Find and click on the specified navigation link
            on the top nav menu.

            :param target: str, link text for link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        top_links = {
            'Home': {
                'sel': 'Home', 'po': 'storyhealth home page',
                'target': '/'
            },
            'Mission' : {
                'sel': 'Mission', 'po': 'storyhealth mission',
                'target': '/mission'
            },
            'About us' : {
                'sel': 'About Us', 'po': 'storyhealth about us',
                'target': '/about-us'
            },
            'Careers' : {
                'sel': 'Careers', 'po': 'storyhealth careers',
                'target': '/careers'
            },
            'Contact' : {
                'sel': 'Contact', 'po': 'storyhealth contact us',
                'target': '/contact'
            },
        }

        # the selector uses the link text
        sel_link = top_links[target]['sel']
        logger.info(f"selector: {sel_link}")

        link_element = self.driver.find_element(By.LINK_TEXT, sel_link)
        po_selector = top_links[target]['po']

        # set the event string
        msg = f"clicked {target} link"
        name = f"link for {target}"
        next_page = self._click_and_load_new_page(link_element,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
