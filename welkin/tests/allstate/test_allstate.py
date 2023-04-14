import pytest
import logging
import time

from welkin.apps.allstate.noauth import pages
from welkin.framework.exceptions import ExpectedPageStateException

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class AllstateTests(object):
    """
        These selenium tests each call a selenium fixture that calls a fresh
        browser instance; that's an architectural decision, that every test
        starts fresh. You could just as easily use one browser session for
        *every* selenium test.

        This selenium fixture is scoped at the function level, and called
        by the test method as `driver`; that fixture is found on:
        welkin/tests/conftest.py::driver()

        pytest fixture documentation:
        https://docs.pytest.org/en/latest/fixture.html
    """
    def test_allstate_navigation(self, driver, allstate):
        """
            Simple navigation flow.

            Use a simple page object model that minimally manages page object
            transitions.

            Note: this is not an actual test, because it has no explicit
            assertions. However, the page object model is performing a
            lot of checks and validations in the background, which allows
            this test case to provide a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the home page object
        home_page = pages.HomePage(driver, firstload=True)
        home_page.save_screenshot('home initialization')  # should be blank

        # load home page in browser and refresh the PO instance
        home_page = home_page.load()
        home_page.save_screenshot('home loaded')

        # click the "sign in" link
        app_login = home_page.switch_to_app()
        app_login.save_screenshot('app login loaded')

    @pytest.mark.parametrize('username',
                             [
                                 'foo',
                                 '@@@@@@',
                                 '    tt'
                             ])
    def test_app_login_error(self, driver, allstate, username):
        """
            Simple error handling checks.

        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        expected_error = 'We didn\'t recognize that username.'
        expected_success = 'We sent a password reset request to your address on file.'

        # instantiate the home page object
        login_page = pages.AppLoginPage(driver, firstload=True)
        login_page.save_screenshot('app login initialization')  # should be blank

        # load home page in browser and refresh the PO instance
        login_page = login_page.load()
        login_page.save_screenshot('app login loaded')

        time.sleep(.5)  # force correct order of screenshots

        # force a login error
        input = username  # just to make this parametrization clear

        try:
            login_page.submit_username(input, expect_error=True)
        except ExpectedPageStateException as error:
            login_page.save_screenshot('app login w/ error')
            logger.info(f"\nactual message: {error.message}")
            assert error.message == expected_error

        # go to forgot password page
        forgot_pw_page = login_page.go_to_forgot_password()
        forgot_pw_page.save_screenshot('forgot password')

        # send the password reset
        new_login_page = forgot_pw_page.submit_username(input, expect_error=False)
        new_login_page.save_screenshot('returned to login page')
