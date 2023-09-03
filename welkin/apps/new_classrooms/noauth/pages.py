import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.new_classrooms.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'new_classrooms'
    domain = 'newclassrooms.org'


class HomePage(BasePage):
    name = 'nc home page'
    # title = 'New Classrooms | We bring together diverse talents and backgrounds to personalize learning for students everywhere.'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        # component-hero-slider component
        # (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Shape the Future of School')]"),
        (True, By.CSS_SELECTOR, "main#mainContent div.component-hero-slider"),
    ]
    unload_checks = [
        # (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Shape the Future of School')]"),
        (True, By.CSS_SELECTOR, "main#mainContent div.component-hero-slider"),
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
        self.title = 'New Classrooms | We bring together diverse talents and backgrounds to personalize learning for students everywhere.'
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


class WhyWeExistPage(BasePage):
    name = 'nc why we exist page'
    title = 'Why we exist - New Classrooms | New Classrooms'
    url_path = '/why-we-exist/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Why we exist')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Why we exist')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SolutionDevelopmentPage(BasePage):
    name = 'nc solution development page'
    title = 'Solution development - New Classrooms | New Classrooms'
    url_path = '/solution-development/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Solution development')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Solution development')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PolicyPage(BasePage):
    name = 'nc policy page'
    title = 'Policy & advocacy - New Classrooms | New Classrooms'
    url_path = '/policy/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Policy & advocacy')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Policy & advocacy')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HistoryPage(BasePage):
    name = 'nc history page'
    title = 'History - New Classrooms | New Classrooms'
    url_path = '/history/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'History')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'History')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class LeadershipPage(BasePage):
    name = 'nc leadership page'
    title = 'Leadership - New Classrooms | New Classrooms'
    url_path = '/leadership/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Leadership')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'Leadership')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class LatestPage(BasePage):
    name = 'nc latest page'
    title = 'The Latest - New Classrooms | New Classrooms'
    url_path = '/the-latest/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'The Latest')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//main[@id='mainContent']//h2[contains(text(), 'The Latest')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
