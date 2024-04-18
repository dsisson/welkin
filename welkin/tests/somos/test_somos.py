import pytest
import logging

from welkin.apps.somos.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class SomosTests(object):
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

    def test_linear_navigation(self, driver, somos):
        """
            Simple navigation flow, using a simple page object model that
            minimally manages page object transitions.

            Note: the page object model is performing a lot of checks and
            validations in the background, which allows this test case to
            provide
            a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        home_page = boot_page.start_with('somos home page')
        home_page.save_screenshot('home loaded')
        assert driver.title == home_page.title

        # handle cookie modal: reject unnecessary cookies
        home_page.select_option_from_cookie_modal('reject')

        id = 'Fraud Mitigation & Data Integrity Solutions'
        fraud_page = home_page.select_page_from_top_menu(id)
        fraud_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == fraud_page.title

        id = 'Routing Optimization'
        routing_page = fraud_page.select_page_from_top_menu(id)
        routing_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == routing_page.title

        id = 'About'
        about_page = routing_page.select_page_from_top_menu(id)
        about_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == about_page.title

        id = 'Our Team'
        our_team_page = about_page.select_page_from_top_menu(id)
        our_team_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == our_team_page.title

        id = 'Insights'
        insights_page = our_team_page.select_page_from_top_menu(id)
        insights_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == insights_page.title

        id = 'Events'
        events_page = insights_page.select_page_from_top_menu(id)
        events_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == events_page.title

        id = 'Home'
        # navigate back to the "Home" page
        home_page = events_page.select_page_from_top_menu(id)
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['Routing Optimization', 'Our Team', 'Fraud Mitigation & Data Integrity Solutions'],
                                ['About', 'Events', 'Our Team'],
                                ['Insights', 'Routing Optimization', 'About'],
                                ['Events', 'Fraud Mitigation & Data Integrity Solutions', 'Home'],
                                ['About', 'Fraud Mitigation & Data Integrity Solutions', 'Insights'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, somos, scenario):
        """
            Dynamic navigation flows. Visit the pages specified in
            the fixture parameter `scenario`.

            Use a simple page object model that minimally manages page object
            transitions.

            Note: this is not an actual test, because it has no explicit
            assertions. However, the page object model is performing a
            lot of checks and validations in the background, which allows
            this test case to provide a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        msg = f"testing navigation path: \nHome --> {'--> '.join(scenario)}"
        logger.info(f"\n{'#' * 60}\n{msg}\n{'#' * 60}\n")

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page
        # to load any other page, we'd need to use its po id
        page = boot_page.start_with('somos home page')
        page.save_screenshot('home loaded')

        # handle cookie modal: reject unnecessary cookies
        page.select_option_from_cookie_modal('reject')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
