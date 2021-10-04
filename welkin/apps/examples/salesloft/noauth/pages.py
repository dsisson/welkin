import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.salesloft.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):

    appname = 'Salesloft'
    domain = 'salesloft.com'


class HomePage(BasePage):

    name = 'salesloft home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="The New Way To Sell"]'),
        # (True, By.XPATH, 'But it doesn’t have to be that way.')
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Can We Help with Your Specific Legal Issue?"]'),
        # title check dynamically added by __init__()
        (False, By.XPATH, 'But it doesn’t have to be that way.')
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
        driver.set_window_size(995, 2200)
        self.driver = driver
        self.title = f"Salesloft: The Leading Sales Engagement Platform"
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


class ConversationsPage(BasePage):

    name = 'salesloft conversations page'
    title = 'Conversation Intelligence: Sales Call Recording & Tracking'
    url_path = '/platform/conversations/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Conversations"]'),
        (True, By.XPATH, '//h2[text()="Call Meeting and Recording"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Conversations"]'),
        (False, By.XPATH, '//h2[text()="Call Meeting and Recording"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class DealsPage(BasePage):

    name = 'salesloft deals page'
    title = 'Sales Meeting Calendaring & Management Tool by Salesloft'
    url_path = '/platform/deals/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Deals"]'),
        (True, By.XPATH, '//h2[text()="Sales Opportunity Management"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Deals"]'),
        (False, By.XPATH, '//h2[text()="Sales Opportunity Management"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContentHubPage(BasePage):

    name = 'salesloft content hub page'
    title = 'Salesloft Content Hub: Insights & Best Practices for Sales Success'
    url_path = '/resources/content-hub/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//div[text()="Welcome to the Salesloft Content Hub"]'),
        (True, By.XPATH, '//div[text()="Featured Post"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//div[text()="Welcome to the Salesloft Content Hub"]'),
        (False, By.XPATH, '//div[text()="Featured Post"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WebinarsPage(BasePage):

    name = 'salesloft webinars page'
    title = 'SalesLoft Webinars: Upcoming & On-Demand Learning'
    url_path = '/resources/webinars/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Webinars"]'),
        (True, By.XPATH, '//h2[text()="Upcoming Webinars"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Webinars"]'),
        (False, By.XPATH, '//h2[text()="Upcoming Webinars"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

