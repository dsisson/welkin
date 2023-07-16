import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.pbsc.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'pbsc'
    domain = 'photoboothsupplyco.com'


class HomePage(BasePage):
    name = 'pbsc home page'
    # title = 'Whole-Person Care Delivered Virtually'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), "
                         "'We help you build a profitable photo booth business')]"),
        (True, By.XPATH, "//h2[contains(text(), "
                         "'Are you struggling to start a business all by yourself?')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), "
                         "'We help you build a profitable photo booth business')]"),
        (True, By.XPATH, "//h2[contains(text(), "
                         "'Are you struggling to start a business all by yourself?')]"),
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
        driver.set_window_size(1285, 2500)
        self.driver = driver
        self.title = 'Profitable Photo Booth Business - Photobooth Supply Co'
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


class ProductSalsaPage(BasePage):
    name = 'pbsc product salsa page'
    title = 'Salsa iPad Photo Booth For Sale - Photobooth Supply Co.'
    url_path = '/products/salsa'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1/p[contains(text(), 'The ultimate iPad')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1/p[contains(text(), 'The ultimate iPad')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProductGuacChipsBoothPage(BasePage):
    name = 'pbsc product quac & chips booth page'
    title = 'Guac iPad Photo Booth For Sale - Photobooth Supply Co.'
    url_path = '/products/guac-chips-photo-booth?view=alt'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1/p[contains(text(), 'Guac & Chips')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1/p[contains(text(), 'Guac & Chips')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProductSalsaSoftwarePage(BasePage):
    name = 'pbsc product salsa software page'
    title = 'Salsa iPad Photo Booth Software - Photobooth Supply Co'
    url_path = '/pages/salsa-software'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'iPad Photo Booth Software')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'iPad Photo Booth Software')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PricingPage(BasePage):
    name = 'pbsc pricing page'
    title = 'Photobooth Software Pricing - Photobooth Supply Co'
    url_path = '/pages/software-pricing'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'Create, capture, and close events')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Create, capture, and close events')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class GuideStartBusinessPage(BasePage):
    name = 'pbsc start a business guide page'
    title = 'How to Start a Photobooth Business - Photobooth Supply Co.'
    url_path = '/pages/how-to-start-a-photobooth-business'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), '6 Steps to 6 Figures')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), '6 Steps to 6 Figures')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
