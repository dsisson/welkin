import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.construct_connect.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'construct_connect'
    domain = 'www.constructconnect.com'


class HomePage(BasePage):
    name = 'construct home page'
    # title = 'Commercial Construction Projects Leads | ConstructConnect'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 've Just Unlocked Our Project Data')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 've Just Unlocked Our Project Data')]"),
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
        self.title = 'Commercial Construction Projects Leads | ConstructConnect'
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


class SubcontractorsPage(BasePage):
    name = 'construct subcontractors page'
    title = 'Construction Leads, Collaborative Takeoff Tools, &amp; Online Bid Board'
    url_path = '/subcontractors'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Find, Bid & Win the Right Projects']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Find, Bid & Win the Right Projects']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class GeneralContractorsPage(BasePage):
    name = 'construct general contractors page'
    title = 'General Contractors | Construction Bid Management Software'
    url_path = '/general-contractors'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Bid Management Made Easy']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Bid Management Made Easy']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BidCenterPage(BasePage):
    name = 'construct bid center page'
    title = 'Bid Center - Commercial Construction Projects Near Me'
    url_path = '/bid-center'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Take Control of Your Bid Pipeline With Bid Center')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Take Control of Your Bid Pipeline With Bid Center')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SurvivalKitPage(BasePage):
    name = 'construct survival kit page'
    title = 'Construction Estimating Survival Kit | ConstructConnect'
    url_path = '/construction-estimating-survival-kit'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Construction Estimating Survival Kit')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Construction Estimating Survival Kit')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CareersPage(BasePage):
    name = 'construct careers page'
    title = 'Careers | ConstructConnect'
    url_path = '/careers'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Impactful Connections   Begin Here']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Impactful Connections   Begin Here']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
