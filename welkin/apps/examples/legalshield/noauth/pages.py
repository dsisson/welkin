import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.legalshield.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):

    appname = 'LegalShield'
    domain = 'www.legalshield.com'


class HomePage(BasePage):

    name = 'legalshield home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[text()="Can We Help with Your Specific Legal Issue?"]')
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Can We Help with Your Specific Legal Issue?"]')
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
        driver.set_window_size(1200, 2200)
        self.driver = driver
        self.title = f"A Better Way to Hire a Lawyer - LegalShield | LegalShield USA"
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


class MissionPage(BasePage):

    name = 'legalshield mission page'
    title = 'Affordable Lawyers Near Me | LegalShield USA'
    url_path = '/why-legalshield/about'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[text()="Who We Are & Our Story"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Who We Are & Our Story"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HowItWorksPage(BasePage):

    name = 'legalshield how it works page'
    title = 'How LegalShield Works | LegalShield USA'
    url_path = '/why-legalshield/how-it-works'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[text()="Your Legal Issues Covered Today and in the Future"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Your Legal Issues Covered Today and in the Future"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PersonalPlanDetailsPage(BasePage):

    name = 'legalshield personal plan details page'
    title = 'Services for LegalShield Personal Legal Plans | LegalShield USA'
    url_path = '/personal-plan/plan-details'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[text()="Legal Help, Made Easy and Affordable"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Legal Help, Made Easy and Affordable"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StartBusinessOverviewPage(BasePage):

    name = 'legalshield start a business overview page'
    title = 'Online Legal Services for Starting a Business | LegalShield USA | LegalShield USA'
    url_path = '/start-a-business'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[text()="Start Your Business the Right Way"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//p[text()="Start Your Business the Right Way"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
