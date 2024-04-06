import logging

from selenium.webdriver.common.by import By

from welkin.apps.clari.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'clari'
    domain = 'www.clari.com'


class HomePage(BasePage):
    name = 'clari home page'
    title = 'Revenue Platform | Clari'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'One unified platform to create, convert, and close')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Reclaim control of the revenue process')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'One unified platform to create, convert, and close')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Reclaim control of the revenue process')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WhyPage(BasePage):
    name = 'clari why page'
    title = 'Why Clari? | Clari'
    url_path = '/why-clari/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'CONSOLIDATE, SIMPLIFY, AND ACCELERATE')]"),
        (True, By.XPATH, "//h2[contains(text(), 'The only unified')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'CONSOLIDATE, SIMPLIFY, AND ACCELERATE')]"),
        (False, By.XPATH, "//h2r[contains(text(), 'The only unified')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProductsCapturePage(BasePage):
    name = 'clari products capture page'
    title = 'Clari Capture - Data Quality and Activity Autocapture | Clari'
    url_path = '/products/capture/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Capture Every Revenue-critical Signal with Clari Capture ')]"),
        (True, By.XPATH, "//h2[contains(text(), 'time back to sell')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Capture Every Revenue-critical Signal with Clari Capture ')]"),
        (False, By.XPATH, "//h2[contains(text(), 'time back to sell')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProductsGroovePage(BasePage):
    name = 'clari products groove page'
    title = 'Groove by Clari - Sales Engagement and Prospecting | Clari'
    url_path = '/products/groove/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Close the Loop between Insights and Action with Groove')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Tailor your engagement')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Close the Loop between Insights and Action with Groove')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Tailor your engagement')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SolutionsUsecasesPage(BasePage):
    name = 'clari solutions usecases page'
    title = 'Solutions by Use Case | Clari'
    url_path = '/solutions/use-cases/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Maximize Revenue Performance at Every Moment, at Every Level')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Boost revenue precision and potential—from frontline to boardroom')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Maximize Revenue Performance at Every Moment, at Every Level')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Boost revenue precision and potential—from frontline to boardroom')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PricingPage(BasePage):
    name = 'clari pricing page'
    title = 'Pricing | Clari'
    url_path = '/pricing/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), '448% ROI via Forrester Total Economic Impact Study')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Mix-and-Match on Clari')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), '448% ROI via Forrester Total Economic Impact Study')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Mix-and-Match on Clari')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1600, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

