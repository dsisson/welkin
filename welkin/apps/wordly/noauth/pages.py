import logging

from welkin.apps.wordly.noauth.base_noauth import NoAuthBasePageObject

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'wordly'
    domain = 'www.wordly.ai'


class HomePage(BasePage):
    name = 'wordly home page'
    title = 'Wordly AI Translation - #1 Meetings and Events Solution'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AiCaptioningPage(BasePage):
    name = 'wordly ai captioning page'
    title = 'What is AI Captioning | Wordly'
    url_path = '/ai-captioning'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class MeetingTranslationPage(BasePage):
    name = 'wordly meeting translation page'
    title = 'Meeting Interpretation Solutions Powered By AI | Wordly'
    url_path = '/meeting-interpretation'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AboutUsPage(BasePage):
    name = 'wordly about us page'
    title = 'Real-time Translation | Powered by Wordly.ai'
    url_path = '/real-time-translation'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WhyWordlyPage(BasePage):
    name = 'wordly why page'
    title = 'Audio Translation | Powered by Wordly.ai'
    url_path = '/audio-translation'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class HowWordlyWorksPage(BasePage):
    name = 'wordly how wordly works page'
    title = 'How Translation Software Powered by AI Works - Wordly'
    url_path = '/translation-software'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AllUseCasesPage(BasePage):
    name = 'wordly all use cases page'
    title = 'Translation Services Customers | Wordly.ai'
    url_path = '/translation-services'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
