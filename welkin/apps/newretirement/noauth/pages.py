import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.newretirement.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'newretirement'
    domain = 'www.newretirement.com'


class HomePage(BasePage):
    name = 'nr home page'
    # title = 'Retirement Calculator and Retirement Planning | NewRetirement'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Take Financial Wellness Into Your Own Hands']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Take Financial Wellness Into Your Own Hands']"),
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
        driver.set_window_size(1285, 2200)
        self.driver = driver
        self.title = 'Retirement Calculator and Retirement Planning | NewRetirement'
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


class HowItWorksPage(BasePage):
    name = 'nr how-it-works page'
    title = 'How It Works | NewRetirement'
    url_path = '/retirement/how-it-works/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='A planning tool that works no matter what life throws at you']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='A planning tool that works no matter what life throws at you']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

class PricingPage(BasePage):
    name = 'nr pricing page'
    title = 'Pricing | NewRetirement'
    url_path = '/retirement/pricing/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), "
                         "'Choose the plan that’s right for you: ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), "
                         "'Choose the plan that’s right for you: ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BlogEarningPage(BasePage):
    name = 'nr blog earning page'
    title = 'Earning Archives | NewRetirement'
    url_path = '/retirement/topic/income/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Earning']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Earning']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ClassesPage(BasePage):
    name = 'nr classes page'
    title = 'Classes Splash Page'
    url_path = '/retirement/classes/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Boost your financial know how ']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Boost your financial know how ']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ApisPage(BasePage):
    name = 'nr apis page'
    title = 'APIs | NewRetirement'
    url_path = '/retirement/enterprise/apis/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Build tools with comprehensive financial projections']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Build tools with comprehensive financial projections']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

