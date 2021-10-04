import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.examples.salesloft.base_page import BaseWrapperPageObject
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
            This is a two-stage navigation interaction
            with the top nav. Click `target1` to open the
            nav pane, then click `target2` to navigate to
            that targeted page.

            :param target1: str, link text for primary link
            :param target2: str, link text for secondary link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        target_links = {
            'Platform': {
                'sel': 'Platform',
                'Conversations': {
                    'sel': '//div[@class="primary-navigation__link-heading" and text()="Conversations"]',
                    'po': 'salesloft conversations page',
                    'target': '/platform/conversations/'
                },
                'Deals': {
                    'sel': '//div[@class="primary-navigation__link-heading" and text()="Deals"]',
                    'po': 'salesloft deals page',
                    'target': '/platform/deals/'
                }
            },
            'Resources': {
                'sel': 'Resources',
                'Content Hub': {
                    'sel': '//a[@class="primary-navigation__link" and text()="Content Hub"]',
                    'po': 'salesloft content hub page',
                    'target': '/resources/content-hub/'
                },
                'Webinars': {
                    'sel': '//a[@class="primary-navigation__link" and text()="Webinars"]',
                    'po': 'salesloft webinars page',
                    'target': '/resources/webinars/'
                }
            },
        }

        # get the primary link element
        primary_link = self.driver.find_element(By.LINK_TEXT,
                                                target_links[target1]['sel'])

        # this is a two-stage action
        # click the link to open the secondary links pane
        event1 = f"clicked {target1} primary link"
        name = f"primary link {target1}"
        self._click_element(primary_link, name, msg=event1)

        # verify that the pane is displayed and inter-actable
        # but this is a demo and we are keeping this quick-n-dirty
        time.sleep(1)

        # get the secondary link element
        try:
            secondary_link = self.driver.find_element(By.XPATH,
                                                      target_links[target1][target2]['sel'])
        except NoSuchElementException:
            self.save_screenshot('first link activated')
            raise

        # get the page object identifier for the target page
        po_selector = target_links[target1][target2]['po']

        # set the event string
        event2 = f"clicked {target2} secondary link"
        name = f"secondary link {target2}"

        # click the secondary link, which will load the new page object
        next_page = self._click_and_load_new_page(secondary_link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True)
        return next_page
