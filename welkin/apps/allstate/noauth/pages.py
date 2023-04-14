import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.allstate.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework.exceptions import ExpectedPageStateException
from welkin.framework.exceptions import UnexpectedPageStateException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):
    appname = 'Allstate'
    domain = 'www.allstateidentityprotection.com'


class BaseAppPage(NoAuthBasePageObject):
    appname = 'AIP app'
    domain = 'app.allstateidentityprotection.com'

class HomePage(BasePage):
    name = 'allstate home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), '
                         '"see how we can help you today")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), '
                          '"see how we can help you today")]'),
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
        driver.set_window_size(1285, 3200)
        self.driver = driver
        self.title = 'Allstate Identity Protection | Discover the Best Protection ' \
                     'for Families | Allstate Identity Protection'
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


class AppLoginPage(BaseAppPage):
    name = 'AIP login page'
    url_path = '/signin'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Welcome")]'),
        (True, By.XPATH, '//span[contains(text(), "Forgot your username?")]'),
    ]
    unload_checks = []

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
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 1200)
        self.driver = driver
        self.title = 'Allstate Identity Protection'
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

    def submit_username(self, data, expect_error=False):
        """
            Ordinarily, this action would support success, but for the
            purposes of this demo, only support unhappy path.

            :param data: *any* data type
            :param expect_error: bool, True means look for errors
            :return:
        """
        name = 'username'
        sel_field = 'bootstrap-input-username'
        field = self.driver.find_element(By.ID, sel_field)

        self._set_field_input(field, name, data, clear=False, click=True,
                              unfocus=False, chunk=False)

        self.save_screenshot('after setting field')
        # submit the search
        self._submit_form_submit(field, name)

        if expect_error:
            # look for error messages
            wait = WebDriverWait(self.driver, 15)
            sel_error = '[data-testid="errorContainer"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel_error)))
            error_message = self.driver.find_element(By.CSS_SELECTOR, sel_error).text
            logger.error(f"\nerror message: {error_message}")
            raise ExpectedPageStateException(error_message)

    def go_to_forgot_password(self):
        po_selector = 'AIP forgot password page'
        sel_forgot_password = 'Forgot your password?'
        link = self.driver.find_element(By.LINK_TEXT, sel_forgot_password)
        next_page = self._click_and_load_new_page(link, 'forgot password',
                                                  po_selector, change_url=True)

        return next_page


class AppForgotPasswordPage(BaseAppPage):
    name = 'AIP forgot password page'
    title = 'Allstate Identity Protection'
    url_path = '/signin/forgot-password'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.XPATH, '//h1[contains(text(), "Reset your password")]'),
    ]
    unload_checks = [
        (False, By.XPATH, '//h1[contains(text(), "Reset your password")]'),
    ]

    def __init__(self, driver):
        self.url = f"https://{self.domain}{self.url_path}"
        driver.set_window_size(1285, 1200)
        self.driver = driver
        logger.info('\n' + INIT_MSG % self.name)

    def submit_username(self, data, expect_error=False):
        """
            Ordinarily, this action would support success, but for the
            purposes of this demo, only support unhappy path.

            :param data: *any* data type
            :param expect_error: bool, True means look for errors
            :return:
        """
        name = 'username'
        sel_field = 'bootstrap-input-username'
        field = self.driver.find_element(By.ID, sel_field)

        self._set_field_input(field, name, data, clear=False, click=True,
                              unfocus=False, chunk=False)

        self.save_screenshot('after setting field')
        # submit the search
        self._submit_form_submit(field, name)

        wait = WebDriverWait(self.driver, 15)
        if expect_error:
            # look for error messages
            sel_error = '[data-testid="errorContainer"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel_error)))
            error_message = self.driver.find_element(By.CSS_SELECTOR, sel_error).text
            logger.error(f"\nerror message: {error_message}")
            raise ExpectedPageStateException(error_message)

        # look for success message
        sel_success = '[data-testid="successContainer"]'
        expected_success_msg = 'We sent a password reset request to your ' \
                               'address on file.'

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel_success)))
        success_message = self.driver.find_element(By.CSS_SELECTOR, sel_success).text
        logger.error(f"\nactual success message: {success_message}")
        if not success_message == expected_success_msg:
            msg = f"Actual success message does NOT match expected " \
                  f"message ('{expected_success_msg}')"
            logger.info(f"\n{msg}")
            raise UnexpectedPageStateException(msg)

        # return the updated PO
        po_selector = 'AIP login page'
        updated_page = self.load_pageobject(po_selector)
        return updated_page

