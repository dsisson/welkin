import logging

from welkin.apps.paytient.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'paytient'
    domain = 'www.paytient.com'


class HomePage(BasePage):
    name = 'paytient home page'
    title = 'Paytient® - Give Your People the Power to Pay for Healthcare'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class EmployersPage(BasePage):
    name = 'paytient employers page'
    title = 'Patient Financing for Employers | Paytient'
    url_path = '/employers'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class InsurersPage(BasePage):
    name = 'paytient insurers page'
    title = 'Health Payment Accounts for Payers | Paytient'
    url_path = '/insurers'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StartPage(BasePage):
    name = 'paytient start page'
    title = 'Member Account Sign-up and Login | Paytient'
    url_path = '/start'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HPAPage(BasePage):
    name = 'paytient what is HPA page'
    title = 'What is a Health Payment Account? | Paytient'
    url_path = '/what-is-a-health-payment-account'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BlogPage(BasePage):
    name = 'paytient blog page'
    title = 'Blog | Paytient'
    url_path = '/blog'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class GuidesPage(BasePage):
    name = 'paytient guides page'
    title = 'Guides'
    url_path = '/guides'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 2500)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
