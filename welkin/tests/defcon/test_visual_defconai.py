import pytest
import logging
from applitools.selenium import Target

from welkin.apps.defcon.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class VisualDefconAiTests(object):
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

    def test_linear_visual_navigation(self, driver, defcon, eyes):
        """
            Simple navigation flow, using a simple page object model that
            minimally manages page object transitions.

            Note: the page object model is performing a lot of checks and
            validations in the background, which allows this test case to
            provide a fairly simple API to page interactions.

            This test method can be run in two ways:
            1. locally, but NOT specifying the grid
            >>>pytest tests/defconai -k test_linear_navigation --browser=headless_chrome

            2. on Aplitools UltraFast Grid
            >>>pytest tests/applitools -k test_linear_navigation --ultrafast_grid=yes
                --browser=headless_chrome

        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        home_page = boot_page.start_with('defcon home page')
        id = 'Home'
        home_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == home_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'MISSION'
        mission_page = home_page.select_page_from_top_menu(id)
        mission_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == mission_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'TEAM'
        team_page = mission_page.select_page_from_top_menu(id)
        team_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == team_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'CAPABILITIES'
        capabilities_page = team_page.select_page_from_top_menu(id)
        capabilities_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == capabilities_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'NEWS'
        news_page = capabilities_page.select_page_from_top_menu(id)
        news_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == news_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'CAREERS'
        careers_page = news_page.select_page_from_top_menu(id)
        careers_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == careers_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'CONTACT US'
        contact_us_page = careers_page.select_page_from_top_menu(id)
        contact_us_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == contact_us_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        # navigate back to the "Home" page
        home_page = contact_us_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

    @pytest.mark.parametrize('scenario',
                            [
                                ['TEAM', 'NEWS', 'MISSION'],
                                ['CAPABILITIES', 'CAREERS', 'TEAM'],
                                ['CAREERS', 'CONTACT US', 'Home'],
                                ['NEWS', 'MISSION', 'NEWS'],
                                ['CONTACT US', 'Home', 'CAPABILITIES'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_visual_navigation(self, driver, defcon, eyes, scenario):
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
        page = boot_page.start_with('defcon home page')
        id = 'Home'
        page.save_screenshot(f"{id.lower()} page loaded")
        assert page.title == driver.title
        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
            assert page.title == driver.title
            # visual test!
            eyes.check(Target.window().fully().with_name(destination))
