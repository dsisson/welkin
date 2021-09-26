import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.storyhealth.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):

    appname = 'storyhealth'
    domain = 'www.storyhealth.ai'   # note the "www"


class HomePage(BasePage):

    name = 'storyhealth home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH,
         '//h1[text()="Empowering Specialists with Adaptive Virtualized Care"]'),
    ]
    unload_checks = [
        (False, By.XPATH,
         '//h1[text()="Empowering Specialists with Adaptive Virtualized Care"]'),
        # title check dynamically added by __init__()
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
        driver.set_window_size(1050, 2200)
        self.driver = driver
        self.title = 'Story Health'
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
            Get and load the home page for storyhealth in the browser
            and instantiate and return a page object for the home page.
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


class MissionPage(BasePage):

    name = 'storyhealth mission'
    title = 'Mission'
    url_path = '/mission'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Our mission is to empower clinicians to deliver their best care to every patient"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Our mission is to empower clinicians to deliver their best care to every patient"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutUsPage(BasePage):

    name = 'storyhealth about us'
    title = 'About Us'
    url_path = '/about-us'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Leading with Healthcare + Tech"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Leading with Healthcare + Tech"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CareersPage(BasePage):

    name = 'storyhealth careers'
    title = 'Careers'
    url_path = '/careers-2'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Join Our Team"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Join Our Team"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContactUsPage(BasePage):

    name = 'storyhealth contact us'
    title = 'Contact'
    url_path = '/contact'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h2[text()="Contact Us"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h2[text()="Contact Us"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
