import logging

from selenium.webdriver.common.by import By

from welkin.apps.transfinder.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'transfinder'
    domain = 'www.transfinder.com'


class HomePage(BasePage):
    name = 'transfinder home page'
    title = 'School Bus Routing Software from Transfinder'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 1700)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ViewfinderPage(BasePage):
    name = 'transfinder viewfinder page'
    title = 'Solutions from Transfinder'
    url_path = '/solutions/Oversee_your_operation_anywhere_anytime'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class TripfinderPage(BasePage):
    name = 'transfinder tripfinder page'
    title = 'Solutions from Transfinder'
    url_path = '/solutions/field_trip_management'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class MarketplacePage(BasePage):
    name = 'transfinder marketplace page'
    title = 'Marketplace | Products & Solutions from Transfinder'
    url_path = '/marketplace/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ProfessionalServicesPage(BasePage):
    name = 'transfinder professional services page'
    title = 'Bus Routing Software Professional Services from Transfinder'
    url_path = '/services/professional-services'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 1900)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutUsPage(BasePage):
    name = 'transfinder about us page'
    title = 'About Us from Transfinder'
    url_path = '/about-us/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 1900)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CaseStudiesPage(BasePage):
    name = 'transfinder case studies page'
    title = 'School bus routing software resources from Transfinder'
    url_path = '/resources/case_studies.cfm'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1100, 4000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
