import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from welkin.apps.magnet.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'magnet'
    domain = 'www.magnetforensics.com'


class HomePage(BasePage):
    name = 'magnet home page'
    title = 'Magnet Forensics | Unlock the Truth. Protect the Innocent.'
    url_path = '/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'Transform Your Approach to Digital Investigations')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Hear What Our Customers Are Saying')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'Transform Your Approach to Digital Investigations')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Hear What Our Customers Are Saying')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class AxiomCyberPage(BasePage):
    name = 'magnet axiom cyber page'
    title = 'Magnet AXIOM Cyber - Magnet Forensics'
    url_path = '/products/magnet-axiom-cyber'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h2[contains(text(), 'AXIOM Cyber Features')]"),
        (True, By.XPATH, "//h3[contains(text(), 'DFIR Tools: Key Considerations & Best Practices')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h2[contains(text(), 'AXIOM Cyber Features')]"),
        (False, By.XPATH, "//h3[contains(text(), 'DFIR Tools: Key Considerations & Best Practices')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class ArtifactIQPage(BasePage):
    name = 'magnet artifact iq page'
    title = 'Magnet ARTIFACT IQ - Immediately Action on Mobile Intelligence'
    url_path = '/products/magnet-artifactiq'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), "
                         "'Immediately Action on Mobile Intelligence')]"),
        (True, By.XPATH, "//h3[contains(text(), "
                         "'SIMPLIFY AND ACCELERATE YOUR INVESTIGATIONS')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), "
                          "'Immediately Action on Mobile Intelligence')]"),
        (False, By.XPATH, "//h3[contains(text(), "
                          "'SIMPLIFY AND ACCELERATE YOUR INVESTIGATIONS')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OfficerWellnessPage(BasePage):
    name = 'magnet officer wellness page'
    title = 'Officer Wellness - Magnet Forensics'
    url_path = '/officer-wellness/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Officer Wellness')]"),
        (True, By.XPATH, "//h3[contains(text(), 'Reducing exposure to CSAM ')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Officer Wellness')]"),
        (False, By.XPATH, "//h3[contains(text(), 'Reducing exposure to CSAM ')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class StrategicPartnersPage(BasePage):
    name = 'magnet strategic partners page'
    title = 'Magnet Technology Partners - Work with Our Partners | Magnet Forensics'
    url_path = '/strategy-partners/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), 'Strategic Partners')]"),
        (True, By.XPATH, "//h2[contains(text(), 'Our Strategic Partners')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), 'Strategic Partners')]"),
        (False, By.XPATH, "//h2[contains(text(), 'Our Strategic Partners')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)


class OurStoryPage(BasePage):
    name = 'magnet our story page'
    title = 'Magnet Forensics | Unlock The Truth. Protect The Innocent.'
    url_path = '/our-story/'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, "//h1[contains(text(), "
                         "'Driving Innovation to Unlock the Truth. Protect the Innocent.')]"),
        (True, By.XPATH, "//h2[contains(text(), 'A Commitment to Justice')]"),
    ]
    unload_checks = [
        (False, By.XPATH, "//h1[contains(text(), "
                          "'Driving Innovation to Unlock the Truth. Protect the Innocent.')]"),
        (False, By.XPATH, "//h2[contains(text(), 'A Commitment to Justice')]"),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1000, 3000)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)
