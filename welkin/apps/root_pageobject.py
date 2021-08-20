import logging
import importlib
import time
import pytest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from welkin.framework.exceptions import PageUnloadException
from welkin.framework.exceptions import PageLoadException
from welkin.framework.exceptions import PageIdentityException
from welkin.framework.exceptions import ControlInteractionException

from welkin.framework import checks
from welkin.framework import utils, utils_file
from welkin.framework import utils_selenium

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
        event = f"loaded page '{po_id}'"

        # perform any page identity checks that are specified in the PO class
        # >> using the new page object! <<
        new_pageobject_instance.verify_self(verbose=True)

        # write the cookies to a file
        new_pageobject_instance.save_cookies()

        # write browser logs to files
        new_pageobject_instance.save_browser_logs()

        # write webstorage to files
        new_pageobject_instance.save_webstorage(event_name=event)

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
            self.save_browser_logs()
            payload = {'page': f"Failed to load page '{self.name}'", 'errors': dict()}
            for validation in found_problems:
                payload['errors'][validation[0]] = validation[1:]
            if screenshot:
                self.save_screenshot('load failure')

            # if this is a SPA, we should grab the session storage and save it

            # finally, raise that exception
            raise PageLoadException(errors=payload)
        else:
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

            :param verbose: bool, whether to output additional logging
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

    def save_screenshot(self, filename=''):
        """
            Wrap the driver's screenshot functionality to generate and save
            the screenshot.

            See welkin/framework/utils.selenium.py::take_and_save_screenshot()
            for more details.

            :param filename: str filename for the screenshot (not including
                             the path)
            :return: None
        """
        fname = filename if filename else self.name
        clean_name = utils.path_proof_name(fname)
        logger.info(f"Generating screenshot for '{clean_name}'.")
        utils_selenium.take_and_save_screenshot(self.driver, clean_name)

    def save_source(self, filename=''):
        """
            Extract and save the page source.

            See welkin/framework/utils.selenium.py::get_and_save_source()
            for more details.

            :param filename: str filename for the source HTML file (not including
                             the path)
            :return: None
        """
        fname = filename if filename else self.name
        clean_name = utils.path_proof_name(fname)
        logger.info(f"Saving page source for '{clean_name}'.")
        utils_selenium.get_and_save_source(self.driver, clean_name)

    def save_cookies(self):
        """
            Get the current page's cookies and save to a file.

            :return: None
        """
        # get the cookies from the driver and save to the PO
        self.cookies = self.driver.get_cookies()

        utils_file.write_cookies_to_file(self.cookies, self.url,
                                         fname=self.name)

    def save_browser_logs(self):
        """
            Grab the Chrome driver console and network logs and write them
            to files.

            :return:
        """
        filename = self.name
        if pytest.welkin_namespace['devtools_supported']:
            # get the logs
            performance_logs = utils_selenium.\
                get_network_traffic_logs(pageobject=self)

            console_logs = {}
            console_logs['console'] = utils_selenium.\
                get_console_logs(pageobject=self)

            logger.info(f"Writing special logs.")

            # write the raw performance logs to /network
            utils_file.write_traffic_log_to_file(log=performance_logs,
                                                 url=self.url, fname=filename)

            # write the scan logs to /console
            utils_file.write_console_log_to_file(log=console_logs,
                                                 url=self.url, fname=filename)

        else:
            logger.warning(f"Cannot access chrome logs for "
                           f"{pytest.welkin_namespace['browser']}.")

    def save_webstorage(self, event_name, filename=None):
        """
            Get the localStorage and sessionStorage for the current page (if
            available), and then write them to logfiles.

            Some data will be stripped out or otherwise cleaned up from the
            output written to the file in the webstorage folder; those rules
            are set in react_utils.py::clean_snapshot_for_react_log()

            :param event_name: str, name of the event
            :param filename: str, custom name for file, if provided
            :return: None
        """
        data = utils_selenium.get_webstorage(self)
        self.set_event(event_name)
        utils_file.write_webstorage_to_files(data,
                                             current_url=self.url,
                                             pageobject_name=self.name,
                                             filename=filename,
                                             event=event_name)

    def set_event(self, event_name):
        """
            Add an event to the current page object's properties.

            An `event` is an interaction with the browser and/or site that
            MAY cause a change in page state by triggering Javascript logic
            to manipulate the DOM.

            For now, we just log the fact of the event.

            :param event_name: str, name of the event
            :return: None
        """
        this_event = {
            '_timestamp': time.time(),
            'event': event_name,
            'page': self.name
        }

        logger.info(f"\nbrowser interaction event:\n{utils.plog(this_event)}")

    # #######################################
    # interaction event wrappers
    # #######################################
    def _unfocus_field(self, name):
        """
            Unfocus a form field by clicking the body tag.

            Note: this will cause problems if the body click
            triggers an interaction.

            :param name: str, identifier for field
            :return: True
        """
        msg = f"Unfocused field '{name}' (clicked 'body')"
        self.driver.find_element(By.TAG_NAME, 'body').click()
        self.set_event(msg)
        return True

    def _set_field_input(self, element, name, content,
                         clear=False, click=True, unfocus=True, chunk=False):
        """
            Wrap the setting of a text input field's value.

            :param element: webdriver form field element
            :param name: str, identifier for field
            :param content: str, content to be entered in field
            :param clear: bool, whether to clear the form field;
                                defaults to False
            :param click: bool, whether to click into the form field;
                                defaults to True
            :param unfocus: bool, whether to unfocus the form field;
                                  defaults to True
            :param chunk: bool, whether to iterate over the content and send
                                each character separately; defaults to False
            :return: True
        """
        if click:
            try:
                element.click()
                msg1 = f"Clicked in field '{name}'"
                self.set_event(msg1)
            except ElementNotVisibleException as e:
                logger.exception(e)
                self.save_screenshot(f"element {name} not visible")
                raise

        if clear:
            old_value = element.get_attribute('value')
            if old_value:
                # only do something if the field is not empty
                self.save_screenshot('before clear')
                try:
                    element = utils_selenium.hard_clear_input_field(self, element, name)
                except ControlInteractionException:
                    err_msg = f"Field '{name}' did not get cleared correctly, " \
                              f"still has value '{old_value}'"
                    logger.error(err_msg)
                    self.save_screenshot(f"{name} field not cleared")
                    raise ControlInteractionException(err_msg)

            # finally we can move on from just clearing the field
            msg2 = f"Cleared field content for {name}"
            logger.info(f"\n---> {msg2}; was \'{old_value}\'")
            self.set_event(msg2)

        if chunk:
            # iterate over the desired value, 1 char at a time
            # drawbacks: takes longer, adds more work
            logger.info(f"\n======> chunking input for '{name}'")
            for i, s in enumerate(content):
                element.send_keys(s)
                logger.info(f"\n======> iteration {i}: set character {s}")
                self.save_screenshot(f"{name} after set {i}")
        else:
            # everything else
            element.send_keys(content)
            msg3 = f"Set field '{name}' with value '{content}'"
            self.set_event(msg3)
            self.save_screenshot('after send keys')

        # get the value and log it
        value = element.get_attribute('value')
        if not value == content:
            # there might be a good reason why the actual doesn't match what
            # was entered, for example field-cleaning logic.
            # Note that it would be too difficult to set expectations here!
            msg = f"the actual value '{value}' doesn't " \
                  f"match the entered value '{content}'"
            logger.warning(f"\n{msg}")

        if unfocus:
            field_map = {
                'date widget': Keys.RETURN,
                'time widget': Keys.ESCAPE
            }

            if field_map.get(name):
                # some fields need special handling because a body click
                # has side effects
                msg = f"Unfocused field '{name}' (sent special key)"
                element.send_keys(field_map[name])
                self.set_event(msg)
            else:
                self._unfocus_field(name)
            self.save_screenshot(f"{name} after unset")

        return True

    def _submit_form_submit(self, element, name):
        """
            Submit a form using the built-in webdriver support for submitting
            the form containing field `element`. This is not strictly a user-
            interaction with the browser.

            Note: the calling method should handle whether this triggers a page
            transition or other page object change.

            :param element: webdriver form field element
            :param name: str, identifier for field
            :return: Trye
        """
        event = f"Submitted form associated with '{name}'"
        element.submit()
        self.set_event(event)