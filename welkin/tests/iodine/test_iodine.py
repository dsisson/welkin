import pytest
import logging

from welkin.apps.iodine.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class iodineTests(object):
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

    def test_linear_navigation(self, driver, iodine):
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

       # navigate to the "why iodine" page
        why_iodine_page = home_page.select_page_from_top_menu('why iodine')
        why_iodine_page.save_screenshot('why iodine page loaded')

       # navigate to the "aware CDI" page
        aware_page = why_iodine_page.select_page_from_top_menu('AwareCDI')
        aware_page.save_screenshot('aware CDI page loaded')

        # navigate to the "interact" page
        interact_page = aware_page.select_page_from_top_menu('Interact')
        interact_page.save_screenshot('interact page loaded')

        # navigate to the "cognitive ML" page
        cognitiveml_page = interact_page.select_page_from_top_menu('CognitiveML')
        cognitiveml_page.save_screenshot('cognitive ML page loaded')

        # navigate to the "chartwise" page
        chartwise_page = cognitiveml_page.select_page_from_top_menu('ChartWiseCDI')
        chartwise_page.save_screenshot('chartwise page loaded')

        # navigate to the "news" page
        news_page = chartwise_page.select_page_from_top_menu('news & insights')
        news_page.save_screenshot('news page loaded')

        # navigate to the "about" page
        about_page = news_page.select_page_from_top_menu('About')
        about_page.save_screenshot('about page loaded')

        # navigate to the "partnerships" page
        partnerships_page = about_page.select_page_from_top_menu('Partnerships')
        partnerships_page.save_screenshot('partnerships page loaded')

        # navigate to the "contact" page
        contact_page = partnerships_page.select_page_from_top_menu('Contact')
        contact_page.save_screenshot('contact page loaded')

        # navigate back to the "Home" page
        home_page = contact_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                            [
                                ['why iodine', 'Interact', 'AwareCDI'],
                                ['news & insights', 'Contact', 'Home', 'Interact', 'AwareCDI'],
                                ['CognitiveML', 'AwareCDI', 'About', 'AwareCDI'],
                                ['Partnerships', 'Interact', 'CognitiveML', 'AwareCDI'],
                                ['Contact', 'news & insights', 'ChartWiseCDI', 'About', 'AwareCDI'],
                                ['Interact', 'why iodine', 'Partnerships', 'AwareCDI']
                             ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05', 'scenario06']
    )
    def test_dynamic_navigation(self, driver, iodine, scenario):
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

        # instantiate the home page object
        # every scenario starts with the home page
        page = pages.HomePage(driver, firstload=True)
        page.save_screenshot('home initialization')  # should be blank

        # load home page in browser and refresh the PO instance
        page = page.load()
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
