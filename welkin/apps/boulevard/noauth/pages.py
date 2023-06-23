import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.boulevard.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'Boulevard'
    domain = 'www.joinblvd.com'

class HomePage(BasePage):
    name = 'boulevard home page'
    # title = 'Boulevard | Software for Salons, Spas & MedSpas'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[starts-with(text(), 'Built for ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[starts-with(text(), 'Built for ')]"),
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
        driver.set_window_size(1285, 4200)
        self.driver = driver
        self.title = 'Boulevard | Software for Salons, Spas & MedSpas'
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


class SalonPage(BasePage):
    name = 'boulevard salon page'
    title = 'Salon Software by Boulevard | #1 Salon Management & POS App'
    url_path = '/salon-software'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'Stunning')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Stunning')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OwnersPage(BasePage):
    name = 'boulevard owners page'
    title = 'For Owners & Managers | Boulevard'
    url_path = '/owners'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text() = 'For Owners and Managers']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text() = 'For Owners and Managers']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class FeaturesPage(BasePage):
    name = 'boulevard features page'
    title = 'Boulevard Features | Client Experience Platform'
    url_path = '/features'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Client Experience Platform?')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Client Experience Platform?')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SelfBookingPage(BasePage):
    name = 'boulevard self-booking page'
    title = 'Client Booking Software | Boulevard'
    url_path = '/features/self-booking'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'sleek as your brand')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'sleek as your brand')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ContactCenterPage(BasePage):
    name = 'boulevard contact center page'
    title = 'Contact Center | Boulevard Client Experience Platform'
    url_path = '/features/contact-center'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'the next level')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'the next level')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class BlogPage(BasePage):
    name = 'boulevard blog page'
    title = 'Boulevard Blog - Salon Management Articles & Tips'
    url_path = '/blog'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'Resources & Blog')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Resources & Blog')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class SuccessStoriesPage(BasePage):
    name = 'boulevard success stories page'
    title = 'Boulevard Blog - Salon Management Articles & Tips'
    url_path = '/blog?resourceId=customer-success-story'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2/span[contains(text(), 'Success Stories')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2/span[contains(text(), 'Success Stories')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OurStoryPage(BasePage):
    name = 'boulevard our story page'
    title = 'About Boulevard | Our Story & Values'
    url_path = '/about'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//button/span[contains(text(), 'Meet Boulevard')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//button/span[contains(text(), 'Meet Boulevard')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class CustomerLovePage(BasePage):
    name = 'boulevard customer love page'
    title = 'Love for Boulevard - Salon Management Software Reviews'
    url_path = '/love'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'From Our Clients')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'From Our Clients')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class PricingPage(BasePage):
    name = 'boulevard pricing page'
    title = 'Plans & Pricing | Boulevard'
    url_path = '/pricing'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Simple and flexible plans that ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Simple and flexible plans that ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
