import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.cyware.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'cyware'
    domain = 'cyware.com'


class HomePage(BasePage):
    name = 'cyware home page'
    # title = 'Dependable Threat Intelligence Solutions from Cyware'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Turn Threat Intelligence Into')]"),
        (True, By.XPATH, "//h1[contains(text(), 'Intelligent Action')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Turn Threat Intelligence Into')]"),
        (False, By.XPATH, "//h1[contains(text(), 'Intelligent Action')]"),
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
        driver.set_window_size(1110, 3000)
        self.driver = driver
        self.title = 'Dependable Threat Intelligence Solutions from Cyware'
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


class IntelExchangeLitePage(BasePage):
    name = 'cyware intel exchange lite page'
    title = 'Threat Intel Exchange Lite | Cyware'
    url_path = '/products/threat-intelligence-lite'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Intel Exchange Lite')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Threat Intel Platform (TIP) Built for Small and Medium-sized Security Teams')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Intel Exchange Lite')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Threat Intel Platform (TIP) Built for Small and Medium-sized Security Teams')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OrchestratePage(BasePage):
    name = 'cyware orchestrate page'
    title = 'User-Friendly Data Security Automation from Cyware | Cyware'
    url_path = '/products/orchestration-automation-platform'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Orchestrate')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Say Goodbye to Legacy SOAR; Automate Security Workflows Within Minutes')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Orchestrate')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Say Goodbye to Legacy SOAR; Automate Security Workflows Within Minutes')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OpenApisPage(BasePage):
    name = 'cyware open apis page'
    title = 'Open APIs Overview | Cyware'
    url_path = '/partners/open-apis'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Open APIs')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Cyware API overview')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Open APIs')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Cyware API overview')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        # unhover is not working correctly for this page
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SecurityGuidesPage(BasePage):
    name = 'cyware security guides page'
    title = 'Cyware Security Guides | Cyber Security & Threat Intelligence Updates | Cyware'
    url_path = '/resources/security-guides'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Security Guides')]"),
        (True, By.XPATH, "//h2[contains(text(), 'What is Cyber Fusion?')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Security Guides')]"),
        (False, By.XPATH, "//h2[contains(text(), 'What is Cyber Fusion?')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CompliancePage(BasePage):
    name = 'cyware compliance page'
    title = 'Cyware Compliance and Certifications | Cyware'
    url_path = '/company/compliance'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Beyond Compliance: A Commitment to Security')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Trust Through Excellence: Certifications & Compliance')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Beyond Compliance: A Commitment to Security')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Trust Through Excellence: Certifications & Compliance')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BlogPage(BasePage):
    name = 'cyware blog page'
    title = 'Cyware Company Blog | Cyber Security & Threat Intelligence Updates | Cyware'
    url_path = '/blog'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Blog')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Recent Posts')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Blog')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Recent Posts')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1110, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
