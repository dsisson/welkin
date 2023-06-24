import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.iodine.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'iodine'
    domain = 'iodinesoftware.com'


class HomePage(BasePage):
    name = 'iodine home page'
    # title = 'iodine | Software for Salons, Spas & MedSpas'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'Healthcare Organizations')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Healthcare Organizations')]"),
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
        self.title = 'Iodine Software - The Future of AI-Enabled Intelligent Care'
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


class WhyIodinePage(BasePage):
    name = 'iodine why page'
    title = 'Why Iodine - Iodine'
    url_path = '/why-iodine/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2/span[contains(text(), 'CognitiveML: the')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2/span[contains(text(), 'CognitiveML: the')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AwareCdiPage(BasePage):
    name = 'iodine aware cdi page'
    title = 'Aware CDI - Iodine'
    url_path = '/aware-cdi/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'End Mid-Cycle')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'End Mid-Cycle')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class InteractPage(BasePage):
    name = 'iodine interact page'
    title = 'Interact - Iodine'
    url_path = '/interact/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'A Better Way to Manage')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'A Better Way to Manage')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CognitiveMlPage(BasePage):
    name = 'iodine cognitiveml page'
    title = 'CognitiveML - Iodine'
    url_path = '/cognitive-ml/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2/b[contains(text(), 'CognitiveML™:')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'CognitiveML™:')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ChartwisePage(BasePage):
    name = 'iodine chartwise page'
    title = 'ChartWiseCDI - Iodine'
    url_path = '/chartwise/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2/b[contains(text(), 'Integrity Made Easy')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Integrity Made Easy')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class NewsInsightsPage(BasePage):
    name = 'iodine news insights page'
    title = 'Insights - Iodine'
    url_path = '/news-and-insights/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'News & Insights')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'News & Insights')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutPage(BasePage):
    name = 'iodine about page'
    title = 'About Us - Iodine'
    url_path = '/about-us/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Meet the Iodine Software Team')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Meet the Iodine Software Team')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PartnershipsPage(BasePage):
    name = 'iodine prtnerships page'
    title = 'Partnerships - Iodine'
    url_path = '/partnerships/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Partnerships')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Partnerships')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContactUsPage(BasePage):
    name = 'iodine contact us page'
    title = 'Contact Us - Iodine'
    url_path = '/contact-us/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), "
                         "'Interested in bringing Iodine Software to your health system?')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), "
                          "'Interested in bringing Iodine Software to your health system?')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

