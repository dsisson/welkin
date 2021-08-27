import pytest
import logging

from welkin.apps.examples.instructure.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class InstructureTests(object):
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
    def test_instructure_navigation(self, driver):
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

        k12_page = home_page.select_page_from_top_menu('K-12')
        k12_page.save_screenshot('k12 loaded')

        higher_ed_page = k12_page.select_page_from_top_menu('HIGHER EDUCATION')
        higher_ed_page.save_screenshot('higher ed loaded')

        # the Resources link loads a canvas page, which is not modeled,
        # se we skip that ;)

        news_page = higher_ed_page.select_page_from_top_menu('NEWS & EVENTS')
        news_page.save_screenshot('news loaded')

        about_page = news_page.select_page_from_top_menu('ABOUT US')
        about_page.save_screenshot('about us loaded')
