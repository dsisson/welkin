import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.tome.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'tome'
    domain = 'tome.app'


class HomePage(BasePage):
    name = 'tome home page'
    # title = 'Tome - shape and share your ideas with AI'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1/span[contains(text(), 'From your mind to theirs,')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1/span[contains(text(), 'From your mind to theirs,')]"),
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
        driver.set_window_size(1285, 2000)
        self.driver = driver
        self.title = 'Tome - shape and share your ideas with AI'
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


class ProductAiPage(BasePage):
    name = 'tome product ai page'
    title = 'AI in Tome – Tome'
    url_path = '/ai'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1/span[contains(text(),"
                         " 'Explore and express')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1/span[contains(text(),"
                         " 'Explore and express')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProductIntegrationsPage(BasePage):
    name = 'tome product integrations page'
    title = 'Integrations – Tome'
    url_path = '/integrations'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Integrations')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Integrations')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class TemplatesPage(BasePage):
    name = 'tome templates page'
    title = 'Templates – Tome'
    url_path = '/templates'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Templates')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Templates')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CommunityPage(BasePage):
    name = 'tome community page'
    title = 'Community – Tome'
    url_path = '/community'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1/span[contains(text(),"
                         " 'Sharing ideas')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1/span[contains(text(),"
                         " 'Sharing ideas')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PricingPage(BasePage):
    name = 'tome pricing page'
    title = 'Pricing – Tome'
    url_path = '/pricing'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Create anything,')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Create anything,')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BlogPage(BasePage):
    name = 'tome blog page'
    title = 'Tome blog – Tome'
    url_path = '/blog'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Tome blog')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='content']//h1[contains(text(),"
                         " 'Tome blog')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
