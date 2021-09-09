import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.dignifi.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):

    appname = 'DigniFi'
    domain = 'www.dignifi.com'


class HomePage(BasePage):

    name = 'dignifi home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Let’s start."]')
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Let’s start."]')
        # title check dynamically added by __init__()
    ]

    def __init__(self, driver, firstload=False):
        """
            Because this is a start page for the application, it needs
            some special handling:
            1. an __init__ arg `firstload` that has to be set as True
               from the test code for the first invocation of the POM.
            2. clearing out the unload_checks if firstload=True

            This special handling works around the fact that the start
            page gets double-loaded, and so the first load can't perform
            unload checks!

            :param driver: webdriver instance
            :param firstload: bool, True if this is a start page first load
        """
        self.url = 'https://' + self.domain
        # increase the browser width in order to display the top nav links
        driver.set_window_size(1110, 2200)
        self.driver = driver
        self.title = f"{self.appname} - Financing for Cars, Motorcycles, and Powersports Vehicles"
        if firstload:
            self.unload_checks = None
            msg = f"Because this is the first load, do NOT check for unload!"
            logger.warning(msg)
        else:
            # because the title is set in __init__(),
            # the check also has to be set and added here
            # note that title is used for the identity check, so we
            # probably don't need ot for a load check
            titlecheck = (False, By.XPATH, f"//title[text()='{self.title}']")
            self.unload_checks.append(titlecheck)
        logger.info(f"\n-----> unload checks: {self.unload_checks}")
        logger.info('\n' + INIT_MSG % self.name)

    def load(self):
        """
            Get and load the home page for Baffle in the browser
            and instantiate and return a page object for the home page.
            In the log record, you will see this page object instantiated
            twice, because the test case called HomePage, and then
            load() called HomePage again to change the browser to the
            appropriate URL.
            :return page: page object for the home page
        """
        self.driver.get(self.url)
        logger.info(f"\nLoaded {self.appname} home page to url '{self.url}'.")

        # instantiate and return a refreshed PO
        po_selector = self.name
        page = self.load_pageobject(po_selector)
        return page


class WhyPage(BasePage):

    name = 'dignifi why page'
    title = 'Why DigniFi - DigniFi'
    url_path = '/why-dignifi-loans/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH,
         '//h1/span[text()="Get on the road"]')
    ]
    unload_checks = [
        (False, By.XPATH,
         '//h1/span[text()="Get on the road"]')
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class FeaturesPage(BasePage):

    name = 'dignifi features and benefits page'
    title = 'DigniFi - Features & Benefits'
    url_path = '/features-and-benefits/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH,
         '//h1[text()="DigniFi ExpressWay can help drive "]')
    ]
    unload_checks = [
        (False, By.XPATH,
         '//h1[text()="DigniFi ExpressWay can help drive "]')
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
