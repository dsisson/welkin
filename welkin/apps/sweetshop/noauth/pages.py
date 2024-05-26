import logging

from selenium.webdriver.common.by import By

from welkin.apps.sweetshop.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'sweetshop'
    domain = 'sweetshop.vivrichards.co.uk'


class HomePage(BasePage):
    name = 'sweetshop home page'
    title = 'Sweet Shop'
    url_path = '/'
    identity_checks = ['check_url']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Welcome to the sweet shop!')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Welcome to the sweet shop!')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SweetsPage(BasePage):
    name = 'sweetshop sweets page'
    title = 'Sweet Shop'
    url_path = '/sweets'
    identity_checks = ['check_url']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Browse sweets')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Browse sweets')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutPage(BasePage):
    name = 'sweetshop about page'
    title = 'Sweet Shop'
    url_path = '/about'
    identity_checks = ['check_url']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Sweet Shop Project')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Sweet Shop Project')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class LoginPage(BasePage):
    name = 'sweetshop login page'
    title = 'Sweet Shop'
    url_path = '/login'
    identity_checks = ['check_url']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Login')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Login')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BasketPage(BasePage):
    name = 'sweetshop basket page'
    title = 'Sweet Shop'
    url_path = '/basket'
    identity_checks = ['check_url']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Your Basket')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Your Basket')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1405, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
