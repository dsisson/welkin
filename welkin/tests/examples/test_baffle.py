import pytest
import logging

from welkin.apps.examples.baffle.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class BaffleTests(object):
    """
        These selenium tests each call a selenium fixture that calls a fresh
        browser instance; that's an architectural decision, that every test
        starts fresh. You could just as easily use one browsersession for
        *every* selenium test.

        This selenium fixture is scoped at the function level, and called
        by the test method as `driver'; that fixture is found on:
        welkin/tests/conftest.py::driver()

        pytest fixture documentation:
        https://docs.pytest.org/en/latest/fixture.html
    """
    def test_baffle_navigation(self, driver):
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

        dps_page = home_page.\
            select_page_from_top_menu(target1='PRODUCT',
                                      target2='Data Protection Services')
        dps_page.save_screenshot('dps page loaded')

        solutions_page = dps_page. \
            select_page_from_top_menu(target1='SOLUTIONS',
                                      target2='Solutions Overview')
        solutions_page.save_screenshot('solutions page loaded')

        resources_page = solutions_page. \
            select_page_from_top_menu(target1='RESOURCES',
                                      target2='Resources Overview')
        resources_page.save_screenshot('resources page loaded')
