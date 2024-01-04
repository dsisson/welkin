import logging

from selenium.webdriver.common.by import By

from welkin.apps.defcon.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'defcon'
    domain = 'www.defconai.com'


class HomePage(BasePage):
    name = 'defcon home page'
    title = 'DEFCON AI - Revolutionizing Contested Mobility Operations'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), ' IN THE FACE OF DISRUPTION')]"),
        (True, By.XPATH, "//h2[contains(text(), 'DEFCON AI IS POSITIONED AT THE INTERSECTION OF ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), ' IN THE FACE OF DISRUPTION')]"),
        (False, By.XPATH, "//h2[contains(text(), 'DEFCON AI IS POSITIONED AT THE INTERSECTION OF ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class MissionPage(BasePage):
    name = 'defcon mission page'
    title = 'Resilience in the Face of Disruption - About DEFCON AI'
    url_path = '/mission'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(),'OUR ')]"),
        (True, By.XPATH, "//h4[contains(text(), 'OUR ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(),'OUR ')]"),
        (False, By.XPATH, "//h4[contains(text(), 'OUR ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class TeamPage(BasePage):
    name = 'defcon team page'
    title = 'Meet our Team – DEFCON AI'
    url_path = '/team'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1/strong[contains(text(),'TEAM')]"),
        (True, By.XPATH, "//h2[contains(text(), 'board of directors')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1/strong[contains(text(),'TEAM')]"),
        (False, By.XPATH, "//h2[contains(text(), 'board of directors')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CapabilitiesPage(BasePage):
    name = 'defcon capabilities page'
    title = 'Our Capabilities - DEFCON AI'
    url_path = '/capabilities'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(),'CAPABILITIES')]"),
        (True, By.XPATH, "//h2[contains(text(), 'NAICS')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(),'CAPABILITIES')]"),
        (False, By.XPATH, "//h2[contains(text(), 'NAICS')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class NewsPage(BasePage):
    name = 'defcon news page'
    title = 'In The News - DEFCON AI Press'
    url_path = '/news'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'NEWS')]"),
        (True, By.XPATH, "//h2/span[contains(text(),'MEDIA')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'NEWS')]"),
        (False, By.XPATH, "//h2/span[contains(text(),'MEDIA')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CareersPage(BasePage):
    name = 'defcon careers page'
    title = 'Join Our Team - DEFCON AI Careers'
    url_path = '/careers'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'JOIN THE ')]"),
        (True, By.XPATH, "//h2[contains(text(), ' POSITIONS')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'JOIN THE ')]"),
        (False, By.XPATH, "//h2[contains(text(), ' POSITIONS')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContactUsPage(BasePage):
    name = 'defcon contact us page'
    title = 'Contact Us - DEFCON AI'
    url_path = '/contact-us'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'CONTACT ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'CONTACT ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(890, 2000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
