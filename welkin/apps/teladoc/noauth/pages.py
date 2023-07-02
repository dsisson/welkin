import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.teladoc.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'teladoc'
    domain = 'www.teladochealth.com'


class HomePage(BasePage):
    name = 'teladoc home page'
    # title = 'Whole-Person Care Delivered Virtually'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Complete care to help you get well. And live well.']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Complete care to help you get well. And live well.']"),
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
        driver.set_window_size(1285, 6000)
        self.driver = driver
        self.title = 'Whole-Person Care Delivered Virtually'
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


class ExpertPrimaryCarePage(BasePage):
    name = 'teledoc expert primary care page'
    title = 'Virtual Primary Care & Online Doctor Visits'
    url_path = '/expert-care/primary-care/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Primary care to become your healthiest self']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Primary care to become your healthiest self']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 6000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ExpertSpecialtyCarePage(BasePage):
    name = 'teledoc expert speciality care page'
    title = 'Virtual Specialty & Wellness Care'
    url_path = '/expert-care/specialty-wellness/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Boost your health with ease']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Boost your health with ease']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 2800)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AdultCarePage(BasePage):
    name = 'teledoc care for adults page'
    title = 'Virtual Care for Adults'
    url_path = '/individuals/adults/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Healthier is possible']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Healthier is possible']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 4800)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OrgsHospitalsVirtualCarePlatformPage(BasePage):
    name = 'teledoc orgs hospital virtual care platform page'
    title = 'Virtual Care Platform for Hospitals & Health Systems'
    url_path = '/organizations/hospitals-health-systems/virtual-care-platform/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Solo™ virtual care platform']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Solo™ virtual care platform']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 3400)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OrgsHealthPlansMentalHealthPage(BasePage):
    name = 'teledoc orgs health plans mental health page'
    title = 'Virtual Mental Health Care for Health Plans'
    url_path = '/organizations/health-plans/mental-health/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Mental health for health plans']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Mental health for health plans']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 3200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OrgsEmployersChronicCarePage(BasePage):
    name = 'teledoc orgs employers chronic care page'
    title = 'Virtual Chronic Care Management for Employers'
    url_path = '/organizations/employers/chronic-care-management/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[text()='Chronic care solutions for employers']"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[text()='Chronic care solutions for employers']"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 3200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

