import logging

from selenium.webdriver.common.by import By

from welkin.apps.examples.instructure.base_page import BaseWrapperPageObject
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

            The `actions` arg could contain pre- and post-actions.
            Here we insert the event string for use downstream.

            :param target: str, link text for link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        top_links = {
            'K-12': {
                'sel': 'k-12', 'po': 'instructure k12 page',
                'target': '/k-12'
            },
            'HIGHER EDUCATION' : {
                'sel': 'higher-education', 'po': 'instructure higher education page',
                'target': '/higher-education'
            },
            'NEWS & EVENTS' : {
                'sel': 'news-events', 'po': 'instructure news & events page',
                'target': '/news-events'
            },
            'ABOUT US' : {
                'sel': 'about', 'po': 'instructure about us page',
                'target': '/about'
            },
        }

        # the selector focuses on end of the href string
        sel_link = f"nav#block-themekit-main-menu a[href$=\"{top_links[target]['sel']}\"]"
        logger.info(f"selector: {sel_link}")

        link_element = self.driver.find_element(By.CSS_SELECTOR, sel_link)
        po_selector = top_links[target]['po']

        # set the event string
        msg = f"clicked {target} link"
        name = f"link for {target}"
        next_page = self._click_and_load_new_page(link_element,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
