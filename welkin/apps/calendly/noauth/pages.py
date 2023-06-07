import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.calendly.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'calendly'
    domain = 'calendly.com'


class HomePage(BasePage):
    name = 'calendly home page'
    # title = 'Free Online Appointment Scheduling Software | Calendly'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        #(True, By.XPATH, '//h1[contains(text(), "Easy scheduling ")]'),
        (True, By.XPATH, '//h2[contains(text(), '
                         '"Share your Calendly availability with others")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Easy scheduling ")]'),
        (False, By.XPATH, '//h2[contains(text(), '
                          '"Share your Calendly availability with others")]'),
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
        self.title = 'Free Online Appointment Scheduling Software | Calendly'
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


class ProductsPage(BasePage):
    name = 'calendly products page'
    title = 'Calendly Features - Workflows, Integrations, Embeds, Routing | Calendly'
    url_path = '/features'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "More than a ")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "More than a ")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SolutionsPage(BasePage):
    name = 'calendly solutions page'
    title = 'Industry Solutions | Calendly'
    url_path = '/solutions'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "A scheduling automation solution for ")]'),
        (True, By.XPATH, '//h2[contains(text(), "Solutions for any industry")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "A scheduling automation solution for ")]'),
        (False, By.XPATH, '//h2[contains(text(), "Solutions for any industry")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class TeamsCompaniesPage(BasePage):
    name = 'calendly teams & companies page'
    title = 'Scheduling for Small and Large Teams | Calendly'
    url_path = '/for-teams'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Smarter scheduling for the whole team")]'),
        (True, By.XPATH, '//h2[contains(text(), "The leader in collaborative scheduling")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Smarter scheduling for the whole team")]'),
        (False, By.XPATH, '//h2[contains(text(), "The leader in collaborative scheduling")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PricingPage(BasePage):
    name = 'calendly pricing page'
    title = 'Pricing | Calendly'
    url_path = '/pricing/2-1'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Pick the perfect plan for your team")]'),
        (True, By.XPATH, '//h4[contains(text(), "Enterprise")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Pick the perfect plan for your team")]'),
        (False, By.XPATH, '//h4[contains(text(), "Enterprise")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ResourcesPage(BasePage):
    name = 'calendly resources page'
    title = 'Resources | Calendly'
    url_path = '/resources'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Explore all of our Resources")]'),
        (True, By.XPATH, '//h4[contains(text(), "E-books & Guides")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Explore all of our Resources")]'),
        (False, By.XPATH, '//h4[contains(text(), "E-books & Guides")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)