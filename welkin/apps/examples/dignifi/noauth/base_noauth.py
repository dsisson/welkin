import logging
import time

from selenium.webdriver.common.by import By

from welkin.apps.examples.dignifi.base_page import BaseWrapperPageObject
from welkin.framework import utils

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def select_page_from_top_menu(self, target1, target2):
        """
            Find and click on the specified `target1` navigation link
            on the top nav menu to open the sub-link modal, then click
            on the specified `target2` link.
            :param target1: str, link text for primary link
            :param target2: str, link text for secondary link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        target_links = {
            'I’m a Consumer': {
                'Why DigniFi': {
                    'sel': "//a/span[text()='I’m a Consumer']",
                    'po': 'dignifi why page',
                    'target': '/why-dignifi-loans/'
                }
            },
            'I’m a Business': {
                'Features & Benefits': {
                    'sel': "//a/span[text()='I’m a Business']",
                    'po': 'dignifi features and benefits page',
                    'target': '/features-and-benefits/'
                }
            },
        }

        # get the primary link element
        primary_link = self.driver.find_element(By.LINK_TEXT, target1)

        # click the link to open the secondary links pane
        event1 = f"clicked {target1} primary link"
        name = f"primary link {target1}"
        self._click_element(primary_link, name, msg=event1)

        # verify that the pane is displayed and inter-actable
        # but this is a demo and we are keeping this quick-n-dirty
        time.sleep(1)

        # get the secondary link element
        secondary_link = self.driver.find_element(By.LINK_TEXT, target2)

        # get the page object identifier for the target page
        po_selector = target_links[target1][target2]['po']

        # click the secondary link, which will load the new page object

        # set the event string
        event2 = f"clicked {target2} secondary link"
        name = f"secondary link {target2}"
        next_page = self._click_and_load_new_page(secondary_link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
    