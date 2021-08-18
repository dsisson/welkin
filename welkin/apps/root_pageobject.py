import logging
import importlib
import time

from selenium.common.exceptions import NoSuchElementException

from welkin.framework.exceptions import PageUnloadException
from welkin.framework.exceptions import PageLoadException
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

            Note: this method controls the change between an old (current)
            page object and the *next* page object. Up until the new class is
            instantiated, `self` refers to the old (current) page object; once
            the new has been instantiated, you must use class instance methods
            and properties of that new page object.

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
        self.verify_unload(screenshot=True, verbose=True)

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

        # instantiate a class instance for the PageObject.
        # Note: at this point, in this method, `self` refers to the old PO
        new_pageobject_instance = pageobject_class(self.driver, **opts)

        # perform any page load checks that are specified in the PO class
        # >> using the new page object! <<
        new_pageobject_instance.verify_load(screenshot=True, verbose=True)

        # perform any page identity checks that are specified in the PO class
        # >> using the new page object! <<
        new_pageobject_instance.verify_self(verbose=True)

        return new_pageobject_instance

    def verify_unload(self, screenshot=False, verbose=False):
        """
            Check that the current page displayed in the browser has unloaded.

            Each page object *may* have a list of specific unload validation
            checks, called `load_checks`. This list contains tuples of methods
            and selectors in the format:
            [(False, By.CSS_SELECTOR, '#layoutVnsContent ul')]

            Remember that the page object model gets out of sync with the
            browser, and this method is a step in re-syncing it by verifying
            that the page that the POM thinks is present has in fact been
            changed.

            The order of events is:
            1. test code calls a PO action which triggers a change in the
               browser, making the PO out of sync with the browser
            2. load_pageobject() is called
            3. unload checks are performed for the current PO <<this method>>
            4. the new PO is instantiated
            5. load checks are performed on the new PO
            6. identity checks are performed on the new PO
            7. the new PO is returned to the test code caller

            :param screenshot: bool, whether to take screenshot if check fails
            :param verbose: bool, determines whether to output additional logging
            :return: True if no problems, else raise PageUnloadException
        """
        # end quickly if no declared unload_checks for this PO
        try:
            self.unload_checks
            if not self.unload_checks:
                # property exists but is empty
                msg = f"\nno unload checks found for {self.name}"
                logger.warning(msg)
                return None
        except AttributeError:
            # property doesn't exist
            msg = f"\nunload checks not found for {self.name}"
            logger.warning(msg)
            return False

        # set up list of found problems; staying empty means no problems found
        found_problems = []
        unload_checks = self.unload_checks
        logger.info(f"\nUnload checks for '{self.name}':\n{unload_checks}.")

        # loop over the unload checks and collect the results
        for check in unload_checks:
            if verbose:
                logger.info(f"\n====> unload check: {check}")
            # `self` below refers to the pageobject
            res = checks.expect_element_to_be_gone(self, check)
            if res:
                # there's problem, so add the check to our collection
                found_problems.append(res)

        if found_problems:
            # loop over the errors and set up PageLoadException object
            errors = {}
            for validation in found_problems:
                errors[validation[0]] = validation[1:]
            if screenshot:
                self.save_screenshot(f"problem unloading {self.name}")

            # finally, raise that exception
            raise PageUnloadException(errors=errors)
        else:
            self.save_screenshot(f"unloaded {self.name}")
            return True

    def verify_load(self, waitfor=30, screenshot=False, verbose=False):
        """
            Check that the current page displayed in the browser
            has completed loading.

            Each page object *may* have a list of specific load validation
            checks, called `load_checks`. This list contains tuples of methods
            and selectors in the format:
            [(False, By.CSS_SELECTOR, '#layoutVnsContent ul')]

            The available load checks are:
                checks.expect_element_to_be_present(): Triggered by `True` as the first value in the self.load_checks
                checks.expect_element_to_be_gone(): Triggered by `False` as the first value in the self.load_checks

            :param waitfor: int, wait time page load verification, defaults to 30 seconds
            :param screenshot: bool, whether to take screenshot if check fails
            :param verbose: bool, determines whether to output additional logging
            :return: True if no problems, else raise PageLoadException
        """
        # end quickly if no declared load_checks for this PO
        try:
            self.load_checks
            if not self.load_checks:
                # property exists but is empty
                msg = f"\nno load checks found for {self.name}"
                logger.warning(msg)
                return None
        except AttributeError:
            # property doesn't exist
            msg = f"\nload checks not found for {self.name}"
            logger.warning(msg)
            return False

        # set up list of found problems; staying empty means no problems found
        found_problems = []
        load_checks = self.load_checks
        logger.info(f"\nLoad checks for '{self.name}':\n{load_checks}.")

        # loop over the load checks and collect the results
        for check in load_checks:
            if verbose:
                logger.info(f"\n====> load check: {check} for '{self.name}'")
            # not pythonic, but also not ambiguous: 'True' means "should be present"
            if check[0] == True:
                res = checks.expect_element_to_be_present(self, check, waitfor)
                if res:
                    # there's problem, so add the check to our collection
                    found_problems.append(res)
            else:  # 'False' means "should NOT be present"
                res = checks.expect_element_to_be_gone(self, check, waitfor)
                if res:
                    # there's problem, so add the check to our collection
                    found_problems.append(res)

        # loop over the errors and set up the PageLoadException object
        if found_problems:
            # save the logs
            logger.info(f"Writing special logs because of load errors")
            # self.get_and_write_logs_to_file()
            payload = {'page': f"Failed to load page '{self.name}'", 'errors': dict()}
            for validation in found_problems:
                payload['errors'][validation[0]] = validation[1:]
            if screenshot:
                self.save_screenshot('load failure')

            # if this is a SPA, we should grab the session storage and save it

            # finally, raise that exception
            raise PageLoadException(errors=payload)
        else:
            # self.get_and_write_logs_to_file()
            return True

    def verify_self(self, verbose=False):
        """
            Check that we are on the expected page by looking at a list of
            possible checks for page elements and values.

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

            :param verbose: bool, determines whether to output additional logging
            :return: True if valid, else raise exception
        """
        logger.info(f"\nAttempting to verify identity for '{self.name}': '{self.driver.current_url}'.")

        # set up list of validation results
        validations = []
        identity_checks = self.identity_checks
        if verbose:
            logger.info(f"\nIdentity checks for page '{self.name}':"
                        f"\n{identity_checks}")

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
                    validations.extend(checks.check_url_chunks(self))  # returns list
            except NoSuchElementException as e:  # exits on first exception
                # we couldn't even find the element we want to use to validate
                # identity, which is a bad sign
                msg = f"\nXXX-> Validation checks failed because couldn't find the element." \
                      f" Probably not on the expected page '{self.name}'; see logs."
                logger.error(msg)
                logger.exception(e)
                self.save_screenshot()
                raise PageIdentityException(errors=msg)

        if False in validations:
            errors = {}
            msg = f"\nXXX-> Self validation checks for page '{self.name}' failed; see logs."
            logger.error(msg)
            logger.info(validations)
            errors['validation'] = msg

            self.save_screenshot(f"error on {self.name}")

            # finally, raise that exception
            raise PageIdentityException(errors=errors)
        else:
            if verbose:
                logger.info(f"\nSuccessfully verified identity for '{self.name}'")
            return True

    def save_screenshot(self, name=''):
        """
            Wrap the driver's screenshot functionality to generate and save
            the screenshot.

            See welkin/framework/utils.selenium.py::take_and_save_screenshot()
            for more details.

            :param name: str filename for the screenshot (not including
                             the path)
            :return: None
        """
        fname = name if name else self.name
        clean_name = utils.path_proof_name(fname)
        logger.info(f"Generating screenshot for '{clean_name}'.")
        utils_selenium.take_and_save_screenshot(self.driver, clean_name)

    def save_source(self, name=''):
        """
            Extract and save the page source.

            See welkin/framework/utils.selenium.py::get_and_save_source()
            for more details.

            :param name: str filename for the source HTML file (not including
                             the path)
            :return: None
        """
        fname = name if name else self.name
        clean_name = utils.path_proof_name(fname)
        logger.info(f"Saving page source for '{clean_name}'.")
        utils_selenium.get_and_save_source(self.driver, clean_name)
