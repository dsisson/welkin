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
    routings_path = 'welkin.apps.cognizant.'
