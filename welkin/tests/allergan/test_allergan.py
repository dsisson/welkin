import pytest
import logging

from welkin.apps.allergan.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class AllerganTests(object):
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
    def test_allergan_navigation(self, driver, allergan):
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

        # navigate to the "Alle" page
        alle_page = home_page.select_page_from_top_menu('Allē')
        alle_page.save_screenshot('alle page loaded')

        # navigate to the "Careers" page
        careers_page = alle_page.select_page_from_top_menu('Careers')
        careers_page.save_screenshot('careers page loaded')

        # navigate back to the home page
        alle_page = careers_page.select_page_from_top_menu('A-DL')
        alle_page.save_screenshot('home page loaded')
