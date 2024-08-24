import logging

from welkin.apps.affinipay.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'affinipay'
    domain = 'www.affinipay.com'


class HomePage(BasePage):
    name = 'affinipay home page'
    title = 'AffiniPay | Practice Management & Fintech for Professionals'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutUsPage(BasePage):
    name = 'affinipay about us page'
    title = 'About AffiniPay: Our Mission, Core Values, and Leadership'
    url_path = '/company/about-us/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class IndustryPerspectivePage(BasePage):
    name = 'affinipay industry perspective page'
    title = 'Industry Perspective: FinTech Trends & Insights'
    url_path = '/industry-perspective/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CareersPage(BasePage):
    name = 'affinipay careers page'
    title = 'AffiniPay Careers | Software & FinTech Jobs in Austin, TX'
    url_path = '/careers/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class NewsroomPage(BasePage):
    name = 'affinipay newsroom page'
    title = 'AffiniPay News: Company Updates and FinTech Industry News'
    url_path = '/company/newsroom/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContactUsPage(BasePage):
    name = 'affinipay contact us page'
    title = 'Contact Us | AffiniPay Customer Service'
    url_path = '/contact-us/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1040, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
