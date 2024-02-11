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
    title = 'Low-Interest Loans Designed For You - Earnest'
    url_path = '/new/homepage'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//header/span[contains(text(), "
                         "'The flexibility you want. The security you need. The care you deserve.')]"),
        (True, By.XPATH, "//h1[contains(text(), 'It’s time to change student lending')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//header/span[contains(text(), "
                         "'The flexibility you want. The security you need. The care you deserve.')]"),
        (False, By.XPATH, "//h1[contains(text(), 'It’s time to change student lending')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StudentLoansPage(BasePage):
    name = 'earnest student loans page'
    title = 'Private Student Loans, Pick What You Pay | Earnest'
    url_path = '/student-loans'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'Private Student Loans')]"),
        (True, By.XPATH, "//h2[contains(text(), 'A financial partner that puts you first')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'Private Student Loans')]"),
        (False, By.XPATH, "//h2[contains(text(), 'A financial partner that puts you first')]"),
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
    url_path = '/new/refinance-student-loans'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//p[contains(text(), 'Refinance Student Loans')]"),
        (True, By.XPATH, "//p[contains(text(), "
                         "'Take control of your student loans. Refinancing could help you pay "
                         "off your debt faster so you can focus on your future.')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//p[contains(text(), 'Refinance Student Loans')]"),
        (False, By.XPATH, "//p[contains(text(), "
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
    title = 'Student Loan Manager I Student Loan Relief I Earnest'
    url_path = '/new/student-loan-manager'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//header[contains(text(), 'Why Earnest Student Loan Manager?')]"),
        (True, By.XPATH, "//header/span[contains(text(), 'Lower payments, less stress')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//header[contains(text(), 'Why Earnest Student Loan Manager?')]"),
        (False, By.XPATH, "//header/span[contains(text(), 'Lower payments, less stress')]"),
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
