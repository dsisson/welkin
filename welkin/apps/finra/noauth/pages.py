import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.finra.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'Finra'
    domain = 'www.finra.org'


class HomePage(BasePage):
    name = 'finra home page'
    title = 'A vibrant market is at its best when it works for everyone. | FINRA.org'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h3[contains(text(), "Creating Opportunity Together")]'),
        (True, By.XPATH, '//h3[contains(text(), "Working to Advance Racial Justice")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h3[contains(text(), "Creating Opportunity Together")]'),
        (False, By.XPATH, '//h3[contains(text(), "Working to Advance Racial Justice")]'),
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
        self.title = 'A vibrant market is at its best when it works for everyone. | FINRA.org'
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


class AboutPage(BasePage):
    name = 'finra about page'
    title = 'About FINRA | FINRA.org'
    url_path = '/about'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "About FINRA")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "About FINRA")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CareersPage(BasePage):
    name = 'finra careers page'
    title = 'Careers | FINRA.org'
    url_path = '/careers'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Careers")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Careers")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class MediaCenterPage(BasePage):
    name = 'finra media center page'
    title = 'Media Center | FINRA.org'
    url_path = '/media-center'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h2[contains(text(), "Latest News")]'),
        (True, By.XPATH, '//h2[contains(text(), "Latest Podcasts")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h2[contains(text(), "Latest News")]'),
        (False, By.XPATH, '//h2[contains(text(), "Latest Podcasts")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class FirmHubPage(BasePage):
    name = 'finra firm hub page'
    title = 'Member Firm Hub | FINRA.org'
    url_path = '/member-firm-hub'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Member Firm Hub")]'),
        (True, By.XPATH, '//h2[contains(text(), "Compliance Resources")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Member Firm Hub")]'),
        (False, By.XPATH, '//h2[contains(text(), "Compliance Resources")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

