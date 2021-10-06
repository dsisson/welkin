import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.owlet.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'Owlet'
    domain = 'owletcare.com'


class HomePage(BasePage):
    name = 'owlet home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//p[@class="h2" and contains(text(), "While they rest easy, you will too.")]'),
        # (True, By.XPATH, 'But it doesn’t have to be that way.')
    ]
    unload_checks = [
        (False, By.XPATH, '//p[@class="h2" and contains(text(), "While they rest easy, you will too.")]'),
        # title check dynamically added by __init__()
    ]

    def __init__(self, driver, firstload=False):
        """
            Because this is a start page for the application, it needs
            some special handling:
            1. an __init__ arg `firstload` that has to be set as True
               from the test code for the first invocation of the POM.
            2. clearing out the unload_checks if firstload=True

            This special handling works around the fact that the start
            page gets double-loaded, and so the first load can't perform
            unload checks!

            :param driver: webdriver instance
            :param firstload: bool, True if this is a start page first load
        """
        self.url = 'https://' + self.domain
        # increase the browser width in order to display the top nav links
        driver.set_window_size(1080, 2200)
        self.driver = driver
        self.title = 'Smart Sock & Baby Monitor: Track Heart Rate, ' \
                     'Oxygen & Sleep – Owlet Baby Care US'
        if firstload:
            self.unload_checks = None
            msg = f"Because this is the first load, do NOT check for unload!"
            logger.warning(msg)
        else:
            # because the title is set in __init__(),
            # the check also has to be set and added here
            # note that title is used for the identity check, so we
            # probably don't need it for a load check
            titlecheck = (False, By.XPATH, f"//title[text()='{self.title}']")
            self.unload_checks.append(titlecheck)
        logger.info(f"\n-----> unload checks: {self.unload_checks}")
        logger.info('\n' + INIT_MSG % self.name)

    def load(self):
        """
            Get and load the home page in the browser, then instantiate and
            return a page object for the home page.

            In the log record, you will see this page object instantiated
            twice, because the test case called HomePage, and then
            load() called HomePage again to change the browser to the
            appropriate URL.

            :return page: page object for the home page
        """
        self.driver.get(self.url)
        logger.info(f"\nLoaded {self.appname} home page to url '{self.url}'.")

        # instantiate and return a refreshed PO
        po_selector = self.name
        page = self.load_pageobject(po_selector)
        return page


class SmartSockPage(BasePage):
    name = 'owlet smart sock page'
    title = 'Smart Sock Monitor for Babies & Toddlers – Owlet Baby Care US'
    url_path = '/products/owlet-smart-sock'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Owlet Smart Sock"]'),
        (True, By.XPATH, '//h2[text()="Tracks Baby’s Heart Rate & Oxygen"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Owlet Smart Sock"]'),
        (False, By.XPATH, '//h2[text()="Tracks Baby’s Heart Rate & Oxygen"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class DreamLabPage(BasePage):
    name = 'owlet dream lab page'
    title = 'Dream Lab: Personalized Baby Sleep Training – Owlet Baby Care US'
    url_path = '/products/dream-lab'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Dream Lab ™ By Owlet"]'),
        # (True, By.XPATH, '//h3[text()="Dream Lab FAQs"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Dream Lab ™ By Owlet"]'),
        #  (False, By.XPATH, '//h3[text()="Dream Lab FAQs"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PregnancyBandPage(BasePage):
    name = 'owlet pregnancy band page'
    title = 'Owlet Band Pregnancy Monitor Beta – Owlet Baby Care US'
    url_path = '/products/band'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="Owlet Pregnancy Band Beta"]'),
        # (True, By.XPATH, '//h3[text()="Dream Lab FAQs"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="Owlet Pregnancy Band Beta"]'),
        #  (False, By.XPATH, '//h3[text()="Dream Lab FAQs"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class WhyOwletPage(BasePage):
    name = 'owlet why page'
    title = 'Why Owlet - Owlet Baby Care US'
    url_path = '/pages/why-owlet'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[text()="For Every Baby"]'),
        # (True, By.XPATH, '//h2[text()="Cam"]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[text()="For Every Baby"]'),
        # (False, By.XPATH, '//h2[text()="Cam"]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
