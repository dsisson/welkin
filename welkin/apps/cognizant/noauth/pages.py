import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.cognizant.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'cognizant'
    domain = 'www.cognizant.com/us/en'


class HomePage(BasePage):
    name = 'cognizant home page'
    # title = 'Intuition engineered—human insight, superhuman speed | Cognizant'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        # component-hero-slider component
        (True, By.XPATH, "//h3[contains(text(), 'Case studies')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[contains(text(), 'Case studies')]"),
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
        self.title = 'Intuition engineered—human insight, superhuman speed | Cognizant'
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


class AutomotivePage(BasePage):
    name = 'cognizant automotive page'
    title = 'Automotive Technology Solutions | Cognizant'
    url_path = '/industries/automotive-technology-solutions'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Shifting transformation into high gear')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Shifting transformation into high gear')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class InsurancePage(BasePage):
    name = 'cognizant insurance page'
    title = 'Insurance Digital Transformation | Cognizant'
    url_path = '/industries/insurance-digital-transformation'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Drive innovation and deliver value')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Drive innovation and deliver value')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class EnterprisePlatformsPage(BasePage):
    name = 'cognizant enterprise platforms page'
    title = 'Enterprise Application Services—CX, Operations & HR | Cognizant'
    url_path = '/services/enterprise-application-services'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1/p[contains(text(), 'Where digital transformation meets business agility')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1/p[contains(text(), 'Where digital transformation meets business agility')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ModernBusinessPage(BasePage):
    name = 'cognizant modern business page'
    title = 'Modern Business—Become Future Ready | Cognizant'
    url_path = '/insights/modern-business'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Becoming future-ready')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Becoming future-ready')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AnnualReportPage(BasePage):
    name = 'cognizant annual report page'
    title = '2022 Annual Report | Cognizant'
    url_path = '/about-cognizant/2022-annual-report'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[contains(text(), 'Building everyday relevance')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[contains(text(), 'Building everyday relevance')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


