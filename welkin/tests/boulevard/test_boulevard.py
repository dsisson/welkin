import pytest
import logging

from welkin.apps.boulevard.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class BoulevardTests(object):
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

    def test_linear_navigation(self, driver, boulevard):
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

       # navigate to the "salon" page
        salon_page = home_page.select_page_from_top_menu('Salon')
        salon_page.save_screenshot('salon page loaded')

       # navigate to the "for owners" page
        owners_page = salon_page.select_page_from_top_menu('For Owners')
        owners_page.save_screenshot('owners page loaded')

        # navigate to the "features" page
        features_page = owners_page.select_page_from_top_menu('Features')
        features_page.save_screenshot('features page loaded')

        # navigate to the "self-booking" page
        selfbooking_page = features_page.select_page_from_top_menu('Self-Booking')
        selfbooking_page.save_screenshot('self-booking page loaded')

        # navigate to the "contact-center" page
        contactcenter_page = selfbooking_page.select_page_from_top_menu('Contact Center')
        contactcenter_page.save_screenshot('contact-center page loaded')

        # navigate to the "blog" page
        blog_page = contactcenter_page.select_page_from_top_menu('Blog')
        blog_page.save_screenshot('blog page loaded')

        """
        need to find better identity signals among the blog pages
        # navigate to the "success stories" page
        successstories_page = blog_page.select_page_from_top_menu('Success Stories')
        successstories_page.save_screenshot('success stories page loaded')
        """

        # navigate to the "our story" page
        our_story_page = contactcenter_page.select_page_from_top_menu('Our Story')
        our_story_page.save_screenshot('our story page loaded')

        # navigate to the "customer love" page
        customer_love_page = our_story_page.select_page_from_top_menu('Customer Love')
        customer_love_page.save_screenshot('our story page loaded')

        # navigate to the "pricing" page
        pricing_page = customer_love_page.select_page_from_top_menu('Pricing')
        pricing_page.save_screenshot('pricing page loaded')

        # navigate back to the "Home" page
        home_page = pricing_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                            [
                                ['Salon', 'Features', 'Pricing'],
                                ['Blog', 'Contact Center', 'Home', 'Features', 'Pricing'],
                                ['Self-Booking', 'Pricing', 'Customer Love', 'Pricing'],
                                ['For Owners', 'Features', 'Self-Booking', 'Pricing'],
                                ['Contact Center', 'Blog', 'Our Story', 'Customer Love', 'Pricing'],
                                ['Features', 'Salon', 'For Owners', 'Pricing']
                             ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05', 'scenario06']
    )
    def test_dynamic_navigation(self, driver, boulevard, scenario):
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
