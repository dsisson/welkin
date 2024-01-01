import pytest
import logging

from welkin.apps.magnet.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class MagnetForensicsTests(object):
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

    def test_linear_navigation(self, driver, magnet):
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

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        home_page = boot_page.start_with('magnet home page')
        home_page.save_screenshot('home loaded')
        home_page.handle_cookie_modal()
        home_page.handle_message()

        # check point
        assert home_page.title == driver.title

        id = 'Magnet AXIOM Cyber'
        axiom_cyber_page = home_page.select_page_from_top_menu(id)
        axiom_cyber_page.save_screenshot(f"{id.lower()} page loaded")
        # check point
        assert axiom_cyber_page.title == driver.title

        id = 'OFFICER WELLNESS'
        officer_wellness_page = axiom_cyber_page.select_page_from_top_menu(id)
        officer_wellness_page.save_screenshot(f"{id.lower()} page loaded")
        # check point
        assert officer_wellness_page.title == driver.title

        id = 'STRATEGIC PARTNERS'
        strategic_partners_page = officer_wellness_page.select_page_from_top_menu(id)
        strategic_partners_page.save_screenshot(f"{id.lower()} page loaded")
        # check point
        assert strategic_partners_page.title == driver.title

        id = 'OUR STORY'
        our_story_page = strategic_partners_page.select_page_from_top_menu(id)
        our_story_page.save_screenshot(f"{id.lower()} page loaded")
        # check point
        assert our_story_page.title == driver.title

        id = 'Magnet ARTIFACT IQ'
        artifact_iq_page = our_story_page.select_page_from_top_menu(id)
        artifact_iq_page.save_screenshot(f"{id.lower()} page loaded")
        # check point
        assert artifact_iq_page.title == driver.title

        # navigate back to the "Home" page
        home_page = artifact_iq_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')
        # check point
        assert home_page.title == driver.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['OUR STORY', 'OFFICER WELLNESS', 'Magnet AXIOM Cyber'],
                                ['Magnet ARTIFACT IQ', 'STRATEGIC PARTNERS', 'OUR STORY'],
                                ['OFFICER WELLNESS', 'Magnet ARTIFACT IQ', 'OFFICER WELLNESS'],
                                ['OFFICER WELLNESS', 'Magnet AXIOM Cyber', 'STRATEGIC PARTNERS'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03', 'scenario04']
    )
    def test_dynamic_navigation(self, driver, magnet, scenario):
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

        # instantiate the home page object
        # every scenario starts with the home page
        page = boot_page.start_with('magnet home page')
        page.save_screenshot('home loaded')
        page.handle_cookie_modal()
        page.handle_message()

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
            # check point
            assert page.title == driver.title
