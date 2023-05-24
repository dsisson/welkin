import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.polywood.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'Polywood'
    domain = 'www.polywood.com'


class HomePage(BasePage):
    name = 'polywood home page'
    # title = 'Outdoor Patio Furniture - Made in The USA - POLYWOOD®'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), '
                         '"POLYWOOD® Furniture Collections to Suit Your Lifestyle")]'),
        (True, By.XPATH, '//h5[contains(text(), "A Sustainable Mission")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), '
                          '"POLYWOOD® Furniture Collections to Suit Your Lifestyle")]'),
        (False, By.XPATH, '//h5[contains(text(), "A Sustainable Mission")]'),
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
        driver.set_window_size(1285, 4200)
        self.driver = driver
        self.title = 'Outdoor Patio Furniture - Made in The USA - POLYWOOD®'
        if firstload:
            self.unload_checks = None
            msg = f"Because this is the first load, do NOT check for unload!"
            logger.warning(msg)
        else:
            # because the title is set in __init__(),
            # the check also has to be set and added here
            # note that title is used for the identity check, so we
            # probably don't need it for a load check
            titlecheck = (False, By.XPATH, f"//title[text()='{self.title}']")
            self.unload_checks.append(titlecheck)
        logger.info(f"\n-----> unload checks: {self.unload_checks}")
        logger.info('\n' + INIT_MSG % self.name)

    def load(self):
        """
            Get and load the home page in the browser, then instantiate and
            return a page object for the home page.

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

    def escape_popup(self):
        wait = WebDriverWait(self.driver, 20)

        sel = '//button[@aria-label="Close form 2"]'
        try:
            link = self.driver.find_element(By.XPATH, sel)

            event1 = f"clicked close modal link"
            name = f"close modal link"

            self._click_element(link, name, msg=event1)
            wait.until_not(EC.visibility_of_element_located((By.XPATH, sel)))
        except NoSuchElementException:
            msg = 'Modal not found.'
            logger.info(msg)


class CategoriesPage(BasePage):
    name = 'polywood categories page'
    title = 'Outdoor Furniture Categories - POLYWOOD®'
    url_path = '/styles.html'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1/span[contains(text(), "Outdoor Furniture Categories")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1/span[contains(text(), "Outdoor Furniture Categories")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CollectionsPage(BasePage):
    name = 'polywood collections page'
    title = 'Outdoor Furniture Collections - POLYWOOD®'
    url_path = '/collections.html'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h2[contains(text(), "Shop by Style")]'),
        (True, By.XPATH, '//h1[contains(text(), "All Collections")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h2[contains(text(), "Shop by Style")]'),
        (False, By.XPATH, '//h1[contains(text(), "All Collections")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class GetInspiredPage(BasePage):
    name = 'polywood get inspired page'
    title = 'Get Inspired - POLYWOOD®'
    url_path = '/get-inspired.html'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1/span/p[contains(text(), "Get Inspired")]'),
        (True, By.XPATH, '//h2/span/p[contains(text(), "More Projects")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1/span/p[contains(text(), "Get Inspired")]'),
        (False, By.XPATH, '//h2/span/p[contains(text(), "More Projects")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class DesignerSeriesPage(BasePage):
    name = 'polywood designer series page'
    title = 'Designer Series - POLYWOOD®'
    url_path = '/designer-series'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1/span[contains(text(), "Welcome To")]'),
        (True, By.XPATH, '//h2[contains(text(), "Details Make The Difference")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1/span[contains(text(), "Welcome To")]'),
        (False, By.XPATH, '//h2[contains(text(), "Details Make The Difference")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

    def escape_popup(self):
        wait = WebDriverWait(self.driver, 20)

        sel = '//button[@aria-label="Close form 3"]'
        try:
            link = self.driver.find_element(By.XPATH, sel)

            event1 = f"clicked close modal link"
            name = f"close modal link"

            self._click_element(link, name, msg=event1)
            wait.until_not(EC.visibility_of_element_located((By.XPATH, sel)))
        except NoSuchElementException:
            msg = 'Modal not found.'
            logger.info(msg)


class ShowroomsPage(BasePage):
    name = 'polywood showrooms page'
    title = 'Where to buy POLYWOOD® Furniture - Showroom Locator'
    url_path = '/showrooms/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Find a Showroom")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Find a Showroom")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
