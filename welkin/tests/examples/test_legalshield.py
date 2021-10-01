import pytest
import logging

from welkin.apps.examples.legalshield.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class LegalShieldTests(object):
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
    def test_legalshield_navigation(self, driver, legalshield):
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

        mission_page = home_page. \
            select_page_from_top_menu(target1='Why LegalShield',
                                      target2='Our Mission')
        mission_page.save_screenshot('mission page loaded')

        howitworks_page = mission_page. \
            select_page_from_top_menu(target1='Why LegalShield',
                                      target2='How it Works')
        howitworks_page.save_screenshot('how it works page loaded')

        plan_details_page = howitworks_page. \
            select_page_from_top_menu(target1='Individuals & Families',
                                      target2='Legal Plan Summary')
        plan_details_page.save_screenshot('personal plan details page loaded')

        overview_page = plan_details_page. \
            select_page_from_top_menu(target1='Start a Business',
                                      target2='Start a Business Overview')
        overview_page.save_screenshot('start business overview page loaded')
