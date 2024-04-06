import pytest
import logging

from welkin.apps.clari.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ClariTests(object):
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

    def test_linear_navigation(self, driver, clari):
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
        home_page = boot_page.start_with('clari home page')
        home_page.save_screenshot('home loaded')
        assert driver.title == home_page.title

        id = 'Why Clari'
        why_page = home_page.select_page_from_top_menu(id)
        why_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == why_page.title

        id = 'Capture'
        capture_page = why_page.select_page_from_top_menu(id)
        capture_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == capture_page.title

        id = 'Groove'
        groove_page = capture_page.select_page_from_top_menu(id)
        groove_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == groove_page.title

        id = 'All Use Cases'
        all_usecases_page = groove_page.select_page_from_top_menu(id)
        all_usecases_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == all_usecases_page.title

        id = 'Pricing'
        pricing_page = all_usecases_page.select_page_from_top_menu(id)
        pricing_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == pricing_page.title

        id = 'Home'
        # navigate back to the "Home" page
        home_page = pricing_page.select_page_from_top_menu(id)
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['Capture', 'All Use Cases', 'Groove'],
                                ['Groove', 'Pricing', 'Why Clari'],
                                ['All Use Cases', 'Why Clari', 'Pricing'],
                                ['Pricing', 'Groove', 'Capture'],
                                ['Why Clari', 'Capture', 'Groove'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, clari, scenario):
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
        page = boot_page.start_with('clari home page')
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
