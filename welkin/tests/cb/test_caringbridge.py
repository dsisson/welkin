import pytest
import logging

from welkin.apps.cb.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class CaringBridgeTests(object):
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

    def test_linear_navigation(self, driver, cb):
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
        home_page = boot_page.start_with('cb home page')
        home_page.save_screenshot('home loaded')
        assert driver.title == home_page.title

        id = 'About Us'
        about_page = home_page.select_page_from_top_menu(id)
        about_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == about_page.title

        # id = 'Our History'
        # history_page = about_page.select_page_from_top_menu(id)
        # history_page.save_screenshot(f"{id.lower()} page loaded")
        # assert driver.title == history_page.title

        id = 'How It Works'
        how_page = about_page.select_page_from_top_menu(id)
        how_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == how_page.title

        id = 'Start A Site'
        start_site_page = how_page.select_page_from_top_menu(id)
        start_site_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == start_site_page.title

        id = 'Advice & Inspiration'
        resources_page = start_site_page.select_page_from_top_menu(id)
        resources_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == resources_page.title

        id = 'Home'
        # navigate back to the "Home" page
        home_page = resources_page.select_page_from_top_menu(id)
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['How It Works', 'About Us', 'Advice & Inspiration'],
                                ['Start A Site', 'Home', 'Advice & Inspiration'],
                                ['About Us', 'Start A Site', 'How It Works'],
                                ['Start A Site', 'About Us', 'Home'],
                                ['How It Works', 'Advice & Inspiration', 'About Us'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, cb, scenario):
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
        page = boot_page.start_with('cb home page')
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
