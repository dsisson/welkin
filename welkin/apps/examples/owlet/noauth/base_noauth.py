import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.examples.owlet.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page as scroll_up

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def select_page_from_top_menu(self, target1, target2=None):
        """
            This is a one- or two-stage navigation interaction
            with the top nav. If just `target1` is supplied, click
            that to navigate to the targeted page. Otherwise,
            click `target1` to open the nav pane, then click
            `target2` to navigate to that targeted page.

            :param target1: str, identifier text for primary link
            :param target2: str, optional identifier text for secondary link
            :return next_page: page object
        """
        # map of targets to selector and PO info
        target_links = {
            'Shop': {
                'sel': '//p[@class="drop_nav-item-title" and text()="Shop"]',
                'Smart Sock Family': {
                    'sel': '//a[contains(@href, "owlet-smart-sock")]/p[text()="Smart Sock 3"]',
                    'po': 'owlet smart sock page',
                    'target': '/products/owlet-smart-sock'
                },
                'Dream Lab': {
                    'sel': '//a[contains(@href, "dream-lab")]/p[text()="Dream Lab"]',
                    'po': 'owlet dream lab page',
                    'target': '/products/dream-lab'
                },
                'Pregnancy Band (Beta)': {
                    'sel': '//a[contains(@href, "band")]/p[text()="Pregnancy Band (Beta)"]',
                    'po': 'owlet pregnancy band page',
                    'target': '/products/band'
                },
            },
            'Why Owlet': {
                'sel': '//p[@class="drop_nav-item-title"]/a[text()="Why Owlet"]',
                'po': 'owlet why page',
                'target': '/pages/why-owlet'
            },
        }

        # get the primary link element
        primary_link = self.driver.find_element(By.XPATH,
                                                target_links[target1]['sel'])

        # this is a hack to avoid writing a "scroll to navbar container" method
        # for this demo...
        scroll_up(self.driver)
        scroll_up(self.driver)
        scroll_up(self.driver)
        self.save_screenshot('after scroll up')

        if not target2:
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

        else:
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

            try:
                # click the secondary link, which will load the new page object
                next_page = self._click_and_load_new_page(secondary_link,
                                                          po_selector=po_selector,
                                                          name=name,
                                                          change_url=True)
            except WebDriverException:
                self.save_screenshot('second link not clickable')
                raise

            return next_page
