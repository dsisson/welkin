import logging

from selenium.webdriver.common.by import By

from welkin.apps.somos.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'somos'
    domain = 'www.somos.com'


class HomePage(BasePage):
    name = 'somos home page'
    title = 'Somos: A Leader in Registry Management & Data Solutions | Somos'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class FraudMitigationPage(BasePage):
    name = 'somos fraud mitigation page'
    title = 'Fraud Mitigation & Data Integrity Solutions | Somos'
    url_path = '/our-solutions'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class RoutingDataPage(BasePage):
    name = 'somos routing data page'
    title = 'Routing Optimization | Somos'
    url_path = '/routing-optimization'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutPage(BasePage):
    name = 'somos about page'
    title = 'Building Stronger Connections between Consumers, Brands and Communities. | Somos'
    url_path = '/about'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OurTeamPage(BasePage):
    name = 'somos our team page'
    title = 'Our Team | Somos'
    url_path = '/about/our-team'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class InsightsPage(BasePage):
    name = 'somos insights page'
    title =  'Insights | Somos'
    url_path = '/insights'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class EventsPage(BasePage):
    name = 'somos events page'
    title =  'Events | Somos'
    url_path = '/events'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1148, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

