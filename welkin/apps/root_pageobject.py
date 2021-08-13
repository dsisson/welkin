import logging
import importlib
import time

from selenium.common.exceptions import NoSuchElementException

from welkin.framework.exceptions import PageIdentityException
from welkin.framework import checks
from welkin.framework import utils, utils_selenium

logger = logging.getLogger(__name__)


class RootPageObject(object):

    def load_pageobject(self, po_id, cross_auth_boundary=False, **opts):
        """
            Load the page object for the page that has been navigated to,
            and return it.

            The importing of the modules and classes has to be done
            dynamically -- and in this method -- in order to avoid
            recursive import loops on start up.

            This uses the data model in the PO's wrapper routings.py for
            a mapping between the page/PO name with the module and
            the object name for that PO.

            What makes this method a little more complicated is the fact
            that the PO instantiation has to be aware of crossing the
            boundary between noauth and auth pages, because those PO
            modules live in separate folders. This boundary is in play
            when logging in from a noauth page (at which point the user
            should be known to the system for subsequent pages), or when
            logging out from an auth page (at which point the user should
            be forgotten by the system).

            The `opts` dict provides a way to feed init args to PO classes
            that require additional data for initialization. Generally
            it's cleaner to have __init__s that only require a webdriver
            instance.

            :param po_id: str, key for the page object in the POM data model
            :param cross_auth_boundary: bool, true to trigger a switch between
                                        auth and noath routing, or vice versa
            :param opts: dict, pass-through parameters for the PO's __init__()
            :return: page object for the target page
        """
        # get the previous page's name; remember that the browser has changed
        # state and we are trying to catch the page object up to the browser
        last_page = self.name

        # unload steps, if needed
        # TODO

        # import the routings module for the appropriate wrapper
        # the path (minus the file name) lives in this wrapper's BasePageObject
        import_path_to_routings = self.routings_path + 'routings'
        logger.info(f"\nPath to routings module for this wrapper:\n{import_path_to_routings}")
        routings = importlib.import_module(import_path_to_routings)

        routing_map = None
        root_path_to_module = None

        # load the correct mapping dict from the wrapper's routings.py file,
        # based on whether the next PO will be noauth or auth
        if self.page_auth_mode == 'noauth':
            if cross_auth_boundary:
                # handle the auth boundary crossing here if needed
                # need to load the auth map
                routing_map = routings.auth_pageobjects
                root_path_to_module = routings.AUTH_PATH
                pass
            else:
                # load the noauth map
                routing_map = routings.noauth_pageobjects
                root_path_to_module = routings.NOAUTH_PATH
        elif self.page_auth_mode == 'auth':
            if cross_auth_boundary:
                # handle the auth boundary crossing here if needed
                # need to load the noauth map
                routing_map = routings.noauth_pageobjects
                root_path_to_module = routings.NOAUTH_PATH
            else:
                # load the auth map
                routing_map = routings.auth_pageobjects
                root_path_to_module = routings.AUTH_PATH
        else:
            msg = f"page_auth_mode can only be 'noauth' or 'auth'; " \
                  f"'{self.page_auth_mode}' is not valid."
            logger.error(msg)
            raise ValueError(msg)

        # get the str module name for the new PO
        page_object_data = routing_map[po_id]

        # assemble the str dot-notation path for the module
        module_path = root_path_to_module + page_object_data['module']

        # dynamically import the module `module_path`
        logger.info(f"\nPath to page object: {module_path} --> '{po_id}'.")
        path_to_module = importlib.import_module(module_path)

        # dynamically translate from the str name of the PO
        # to the PO's class
        pageobject_class = getattr(path_to_module, page_object_data['object'])

        # instantiate a class instance for the PageObject
        new_pageobject_instance = pageobject_class(self.driver, **opts)

        # perform any page load checks that are specified in the PO class
        # TODO

        # perform any page identity checks that are specified in the PO class
        new_pageobject_instance.verify_self()

        return new_pageobject_instance

    def verify_self(self, take_screenshot=True):
        """
            Check that we are on the expected page by looking at a list of
            possible checks for page elements and values.

            Before any checks are made, we use the loading of the terms link
            in the page footer as a weak validation that the shell of the page
            has loaded. We should find a better proxy, because this will not
            catch if the elements in the body of the page have not loaded
            or rendered.

            Each page object sets a list of checks, called `checks`. This list
            contains strings corresponding to individual validations to perform
            here in verify_self().

            Extending the kinds of checks we do should be as simple as adding
            a check method below, and adding the data to the affected page
            object classes, and adding the string check name to that PO's
            checks list.

            In the event of validation errors, also check for displayed error
            messages. If found, push those messages into the raised
            PageIdentityException. These messages indicate that the page
            reloaded on submit.

            :param take_screenshot: bool, whether to take a screenshot on
                                          validation error
            :return: True if valid, else raise exception
        """
        logger.info(f"Verifying '{self.name}': '{self.driver.current_url}'.")

        # write the cookies to a file
        # self.save_cookies()

        # set up list of validation results
        validations = []
        identity_checks = self.identity_checks

        # check for an error page
        if 'Error' in self.driver.title:
            # self.take_screenshot(name=f"{self.name}_error")
            logger.error(f"Instead of '{self.name}' page got error page; check screenshot.")
            raise PageIdentityException

        # check whether the page has finished loading; this will raise an exception if not loaded
        # self.verify_load(waitfor=WAITFOR, take_screenshot=take_screenshot)

        # collect the results of the checks
        for id_check in identity_checks:
            try:
                if id_check == 'check_title':
                    validations.append(checks.check_title(self))
                elif id_check == 'check_url':
                    validations.append(checks.check_url(self))
                elif id_check == 'check_exact_url':
                    validations.append(checks.check_exact_url(self))
                elif id_check == 'check_url_chunks':
                    validations.extend(checks.check_url_chunks(self))  # dealing with a returned list
            except NoSuchElementException as e:  # this will exit on the first exception
                # we couldn't even find the element we want to use to validate
                # identity, which is a bad sign
                msg = f"Validation checks failed because couldn't find the element." \
                      f" Probably not on the expected page '{self.name}'; see logs."
                logger.error(msg)
                logger.exception(e)
                self.save_screenshot()

                raise PageIdentityException(errors=msg)

        if False in validations:
            errors = {}
            msg = f"Self validation checks for page '{self.name}' failed; see logs."
            logger.error(msg)
            logger.info(validations)
            errors['validation'] = msg

            self.save_screenshot(f"error on {self.name}")

            # finally, raise that exception
            raise PageIdentityException(errors=errors)
        else:
            event = f"page load for {self.name}"
            return True

    def save_screenshot(self, name=''):
        """
            Wrap the driver's screenshot functionality to generate and save
            the screenshot.

            See welkin/framework/utils.selenium.py::take_and_save_screenshot
            for more details.

            :param name: str filename for the screenshot (not including
                             the path)
            :return: None
        """
        fname = name if name else self.name
        clean_name = utils.path_proof_name(fname)
        logger.info(f"Generating screenshot for '{clean_name}'")
        utils_selenium.take_and_save_screenshot(self.driver, clean_name)
