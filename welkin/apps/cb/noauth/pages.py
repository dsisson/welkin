import logging

from selenium.webdriver.common.by import By

from welkin.apps.cb.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'cb'
    domain = 'www.caringbridge.org'


class HomePage(BasePage):
    name = 'cb home page'
    title = 'Personal Health Journals for Any Condition | CaringBridge'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(text(), 'Share Your Story')]"),
        (True, By.XPATH, "//div[contains(text(), 'Give Together')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(text(), 'Share Your Story')]"),
        (False, By.XPATH, "//div[contains(text(), 'Give Together')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutPage(BasePage):
    name = 'cb about page'
    title = 'About Us | CaringBridge'
    url_path = '/about-us'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(concat(' ', normalize-space(@class), ' '), ' media-header-1 ')]//h1[contains(text(), 'Our Vision & Mission')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Impact & Reach')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(concat(' ', normalize-space(@class), ' '), ' media-header-1 ')]//h1[contains(text(), 'Our Vision & Mission')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Impact & Reach')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HistoryPage(BasePage):
    name = 'cb history page'
    title = 'Our History'
    url_path = '/about-us/history'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH,
         "//div[@class='media-header-1']/h1[contains(text(), 'History of CaringBridge')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Expanding Our Reach')]"),
    ]
    unload_checks = [
        (False, By.XPATH,
         "//div[@class='media-header-1']/h1[contains(text(), 'History of CaringBridge')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Expanding Our Reach')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HowItWorksPage(BasePage):
    name = 'cb how it works page'
    title = 'How It Works | CaringBridge'
    url_path = '/how-it-works'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(),'How It Works')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Choose Your Privacy Settings')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(),'How It Works')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Choose Your Privacy Settings')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StartASitePage(BasePage):
    name = 'cb start a site page'
    title = 'Create Your CaringBridge Website | Health Journal | CaringBridge'
    url_path = '/createwebsite'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(),'CaringBridge has a')]"),
        (True, By.XPATH, "//h1[contains(text(), 'New and Improved Experience!')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(),'CaringBridge has a')]"),
        (False, By.XPATH, "//h1[contains(text(), 'New and Improved Experience!')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ResourcesPage(BasePage):
    name = 'cb resources page'
    title = 'Advice & Inspiration | CaringBridge'
    url_path = '/resources'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(),'Advice & Inspiration')]"),
        (True, By.XPATH,
         "//h2[contains(text(), 'Are you a CaringBridge Site Author or Co-Author?')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(),'Advice & Inspiration ')]"),
        (False, By.XPATH,
         "//h2[contains(text(), 'Are you a CaringBridge Site Author or Co-Author?')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
