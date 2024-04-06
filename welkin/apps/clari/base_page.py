import logging

from welkin.apps.root_pageobject import RootPageObject

logger = logging.getLogger(__name__)


class BaseWrapperPageObject(RootPageObject):
    """
        the typical package structure for a POM wrapper is:
        apps
            |- package
                |- routings.py
                |- base_page.py
                    |- noauth (for pages that do not require authentication)
                        |- base_noauth.py
                    |- auth  (for pages that DO require authentication)
                        |- base_auth.py

        In order for load_pageobjects() to work, it needs to be called
        with args for
        1. the wrapper's path to its routings.py file; this file is used to
           map the po selector string ID to the class name, which in turn
           allows the instantiation of the new PO object.
        2. the wrapper's path to the module files, which will typically be
           in two buckets: pages that do NOT require authentication, and
           those pages that DO require authentication. The distinction is
           important because pages behind the auth barrier have access to
           user data and typically display personalized to the user
           information.
    """
    # the path to the routings file for this app wrapper
    routings_path = 'welkin.apps.clari.'


class PomBootPage(BaseWrapperPageObject):
    """
        This class is the booter for a page object model.

        This class has to be included in a wrapper's routings.py file, e,g.:
            'POM boot page': {
                'module': 'base_page',
               'object': 'PomBootPage',
                'path': 'welkin.apps.<wrapper>.'
            },

        Example usage:
        >>> from welkin.apps.sweetshop.base_page import PomBootPage
        >>> boot_page = PomBootPage(driver)
        >>> home_page = boot_page.start_with('sweetshop home page')
    """
    page_auth_mode = 'noauth'
    name = 'POM boot page'
    title = ''
    url = 'data:,'
    identity_checks = ['check_exact_url']
    load_checks = None
    unload_checks = None

    def __init__(self, driver):
        self.driver = driver
        driver.set_window_size(1600, 2000)
        logger.info('\nInstantiated boot PageObject.')

    def start_with(self, page_id):
        """
            For the supplied `page_id`, figure out the url for that
            page and load that in the driver, then instantiate the page
            object for that page, then return that page object.

            This is the mechanism to create the wrapper's page object model
            that keeps the test code in sync with the browser's state.

            :param page_id: str, key for the page object in the POM data model
            :return new_pageobject_instance: page object for the target page
        """
        # step 1: using the page id, instantiate that page's pageobject
        page = self.resolve_pageobject(po_id=page_id)

        # step 2: from that page object instance, get the url for that page
        target_url = page.url

        # step 3: load the page in the browser using webdriver
        self.driver.get(target_url)

        # step 4: update the POM based on what we think the browser just did;
        # we can be pretty sure of what we told the browser to do, and we hope
        # we understand how the context has changed, but we don't KNOW that the
        # was loaded correctly into the browser. So, we re-load the pageobject
        # with the checks.
        new_pageobject_instance = self.load_pageobject(po_id=page_id)

        # step 5: return the page object to the calling test code
        return new_pageobject_instance
