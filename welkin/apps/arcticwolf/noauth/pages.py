import logging

from selenium.webdriver.common.by import By

from welkin.apps.arcticwolf.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'arcticwolf'
    domain = 'arcticwolf.com'


class HomePage(BasePage):
    name = 'arcticwolf home page'
    title = 'Arctic Wolf | The Leader in Security Operations'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'The Leader in Security Operations')]"),
        (True, By.XPATH, "//h1[contains(text(), 'Concierge Delivery Model')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'The Leader in Security Operations')]"),
        (False, By.XPATH, "//h1[contains(text(), 'Concierge Delivery Model')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SolutionsPage(BasePage):
    name = 'arcticwolf solutions page'
    title = 'Solutions - Boost Your Security Posture | Arctic Wolf'
    url_path = '/solutions/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' elementor-widget-heading ')]//h1[contains(text(), 'Solutions')]"),
        (True, By.XPATH, "//h3[contains(text(), 'SECURITY OPERATIONS AS A CONCIERGE SERVICE')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' elementor-widget-heading ')]//h1[contains(text(), 'Solutions')]"),
        (False, By.XPATH, "//h3[contains(text(), 'SECURITY OPERATIONS AS A CONCIERGE SERVICE')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HowItWorksPage(BasePage):
    name = 'arcticwolf how it works page'
    title = 'How it Works | Arctic Wolf'
    url_path = '/how-it-works/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(text(), 'Broad Visibility')]"),
        (True, By.XPATH, "//h1[contains(text(), 'The Arctic Wolf')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(text(), 'Broad Visibility')]"),
        (False, By.XPATH, "//h1[contains(text(), 'The Arctic Wolf')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WhyPage(BasePage):
    name = 'arcticwolf why page'
    title = 'Why Arctic Wolf?'
    url_path = '/why-arctic-wolf/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Why Arctic Wolf?')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Experience the Security Operations Approach ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Why Arctic Wolf?')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Experience the Security Operations Approach ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ResourceCenterPage(BasePage):
    name = 'arcticwolf resource center page'
    title = 'Resource Center - Arctic Wolf'
    url_path = '/resources/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Resource Center')]"),
        (True, By.XPATH, "//section//div[contains(text(), 'Subscribe to our Monthly Newsletter')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Resource Center')]"),
        (False, By.XPATH, "//section//div[contains(text(), 'Subscribe to our Monthly Newsletter')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PartnersProvidersPage(BasePage):
    name = 'arcticwolf partners providers page'
    title = 'Arctic Wolf for Solution Providers - Arctic Wolf'
    url_path = '/partners/solution-providers/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' elementor-widget-heading ')]//h1[contains(text(), 'Arctic Wolf for Solution Providers')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Managed Detection and Response')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' elementor-widget-heading ')]//h1[contains(text(), 'Arctic Wolf for Solution Providers')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Managed Detection and Response')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CompanyLeadershipPage(BasePage):
    name = 'arcticwolf company leadership page'
    title = 'Company Leadership | Arctic Wolf'
    url_path = '/company/companyleadership/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//section//span[contains(text(), 'Executive Leadership')]"),
        (True, By.XPATH, "//ul[@id='leadership-nav']//a[@href='#board-of-directors']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//section//span[contains(text(), 'Executive Leadership')]"),
        (False, By.XPATH, "//ul[@id='leadership-nav']//a[@href='#board-of-directors']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

