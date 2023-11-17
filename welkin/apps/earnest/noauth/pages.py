import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.earnest.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'earnest'
    domain = 'www.earnest.com'


class HomePage(BasePage):
    name = 'earnest home page'
    # title = 'Low-Interest Loans Designed For You - Earnest'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'WELCOME TO EARNEST')]"),
        (True, By.XPATH, "//h1[contains(text(), 'It’s time to change student lending')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'WELCOME TO EARNEST')]"),
        (False, By.XPATH, "//h1[contains(text(), 'It’s time to change student lending')]"),
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
        driver.set_window_size(1405, 2000)
        self.driver = driver
        self.title = 'Low-Interest Loans Designed For You - Earnest'
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


class StudentLoansPage(BasePage):
    name = 'earnest student loans page'
    title = 'Private Student Loans, Pick What You Pay | Earnest'
    url_path = '/student-loans'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'Private Student Loans')]"),
        (True, By.XPATH, "//h1[contains(text(), 'Seriously simple.')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'Private Student Loans')]"),
        (False, By.XPATH, "//h1[contains(text(), 'Seriously simple.')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ParentLoansPage(BasePage):
    name = 'earnest parent loans page'
    title = 'Private Parent Loans for College - Lower Rates, No Fees - Earnest'
    url_path = '/student-loans/parent-loans'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'Private Parent Loans ')]"),
        (True, By.XPATH, "//h1[contains(text(), 'Make college dreams a reality')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'Private Parent Loans ')]"),
        (False, By.XPATH, "//h1[contains(text(), 'Make college dreams a reality')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ResourcesPage(BasePage):
    name = 'earnest resources page'
    title = 'Resources - Earnest'
    url_path = '/resources'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Resources')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Resources')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class RefinanceStudentLoansPage(BasePage):
    name = 'earnest refinance student loans page'
    title = 'Refinance Student Loans: Rated 5/5 on NerdWallet - Earnest'
    url_path = '/refinance-student-loans'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'REFINANCE STUDENT LOANS')]"),
        (True, By.XPATH, "//div[contains(text(), "
                         "'Take control of your student loans. Refinancing could help you pay "
                         "off your debt faster so you can focus on your future.')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'REFINANCE STUDENT LOANS')]"),
        (False, By.XPATH, "//div[contains(text(), "
                         "'Take control of your student loans. Refinancing could help you pay "
                         "off your debt faster so you can focus on your future.')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StudentLoanManagerPage(BasePage):
    name = 'earnest student loan manager page'
    title = 'Student Loan Manager - Live - Earnest'
    url_path = '/student-loan-manager'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'Student Loan Manager')]"),
        (True, By.XPATH, "//h1[contains(text(), 'Lower payments, less stress')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'Student Loan Manager')]"),
        (False, By.XPATH, "//h1[contains(text(), 'Lower payments, less stress')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CalculatorDebtIncomePage(BasePage):
    name = 'earnest debt-to-income calculator page'
    title = 'Debt-to-Income Ratio Calculator - [How to Calculate Your DTI Ratio] | Earnest'
    url_path = '/debt-to-income-ratio-calculator'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(text(), 'Debt To Income Ratio Calculator')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Check the health of your monthly cashflow')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(text(), 'Debt To Income Ratio Calculator')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Check the health of your monthly cashflow')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
