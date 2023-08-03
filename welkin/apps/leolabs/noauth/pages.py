import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.leolabs.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'leolabs'
    domain = 'leolabs.space'


class HomePage(BasePage):
    name = 'leolabs home page'
    # title = 'Whole-Person Care Delivered Virtually'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//header//h1[contains(text(), 'It’s a life cycle: the complex world of space safety explained')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//header//h1[contains(text(), 'It’s a life cycle: the complex world of space safety explained')]"),
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
        driver.set_window_size(1285, 4000)
        self.driver = driver
        self.title = 'LeoLabs | Propelling the dynamic space era'
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


class LeotrackPage(BasePage):
    name = 'leolabs LeoTrack page'
    title = 'LeoTrack - LeoLabs'
    url_path = '/leotrack/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='LeoTrack is a web-based, off-the-shelf service providing automated, independent monitoring for satellites.']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='LeoTrack is a web-based, off-the-shelf service providing automated, independent monitoring for satellites.']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class RadarsPage(BasePage):
    name = 'leolabs radars page'
    title = 'Our Radars - LeoLabs'
    url_path = '/radars/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='Explore our global radar network']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='Explore our global radar network']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class VertexPage(BasePage):
    name = 'leolabs vertex page'
    title = 'Our Vertex - LeoLabs'
    url_path = '/vertex/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='Introducing Vertex — our space operations stack']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='Introducing Vertex — our space operations stack']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class RegulatorsPage(BasePage):
    name = 'leolabs regulators page'
    title = 'Regulators - LeoLabs'
    url_path = '/regulators/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='The dynamic space era is bringing new possibilities, innovations, and challenges — are you prepared?']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='The dynamic space era is bringing new possibilities, innovations, and challenges — are you prepared?']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class InsurersPage(BasePage):
    name = 'leolabs insurers page'
    title = 'Insurers - LeoLabs'
    url_path = '/insurers/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='We’re living in a dynamic space era.']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='We’re living in a dynamic space era.']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class LeoPulsePage(BasePage):
    name = 'leolabs LeoPulse page'
    title = 'LeoPulse - LeoLabs'
    url_path = '/leopulse/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='LEO is always changing, but you can keep up ']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='LEO is always changing, but you can keep up ']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutUsPage(BasePage):
    name = 'leolabs about us page'
    title = 'About Us - LeoLabs'
    url_path = '/about-us/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h3[text()='Unparalleled coverage, unmatched speed, unlimited insights']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h3[text()='Unparalleled coverage, unmatched speed, unlimited insights']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
