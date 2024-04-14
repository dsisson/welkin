import logging

from selenium.webdriver.common.by import By

from welkin.apps.tetra.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'tetra'
    domain = 'www.tetrascience.com'


class HomePage(BasePage):
    name = 'tetra home page'
    title = 'Tetra Scientific Data and AI Cloud | TetraScience'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'The Scientific Data ')]"),
        (True, By.XPATH, "//h2[contains(text(), 'only data and AI cloud built for science')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'The Scientific Data ')]"),
        (False, By.XPATH, "//h2[contains(text(), 'only data and AI cloud built for science')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WhyPage(BasePage):
    name = 'tetra why page'
    title = 'Why Tetra | TetraScience'
    url_path = '/why-tetra'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Scientific AI is the key to solving humanity’s grand challenges')]"),
        (True, By.XPATH, "//h2[contains(text(), 'The hope and hype of ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Scientific AI is the key to solving humanity’s grand challenges')]"),
        (False, By.XPATH, "//h2[contains(text(), 'The hope and hype of ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class DataReplatformingPage(BasePage):
    name = 'tetra data replatforming page'
    title = 'Scientific Data Replatforming | TetraScience'
    url_path = '/platform/data-replatforming'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Collect, centralize, and contextualize all your scientific data')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Automate your scientific data assembly in the cloud')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Collect, centralize, and contextualize all your scientific data')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Automate your scientific data assembly in the cloud')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class QualityPage(BasePage):
    name = 'tetra quality page'
    title = 'Protect Quality and Compliance | Benefits for Regulatory Leaders | TetraScience'
    url_path = '/solutions/quality'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Protect quality and compliance')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Lay the foundation for quality')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Protect quality and compliance')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Lay the foundation for quality')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class TetraDataPage(BasePage):
    name = 'tetra data page'
    title = 'The World’s Only Open, Collaborative, AI-native Scientific Data | TetraScience'
    url_path = '/tetra-data'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Tetra Data is the atomic building block of Scientific AI ')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Replatformed data')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Tetra Data is the atomic building block of Scientific AI ')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Replatformed data')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class FlowCytometryPage(BasePage):
    name = 'tetra flow cytometry page'
    title = 'Biologics Screening Flow Cytometry | TetraScience'
    url_path = '/scientific-outcomes/biologics-screening-flow-cytometry'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Accelerate and improve biologics screening by flow cytometry')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Unlock the full value of your flow cytometry data')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Accelerate and improve biologics screening by flow cytometry')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Unlock the full value of your flow cytometry data')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class NewsroomPage(BasePage):
    name = 'tetra newsroom page'
    title = 'Latest News and Announcements | TetraScience Newsroom'
    url_path = '/company/news'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'TetraScience Newsroom')]"),
        (True, By.XPATH, "//div[contains(text(), 'Press Release')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'TetraScience Newsroom')]"),
        (False, By.XPATH, "//div[contains(text(), 'Press Release')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1232, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
