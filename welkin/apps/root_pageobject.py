import logging
import importlib
import time
import pytest
from axe_selenium_python import Axe

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException

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

            Also note: a *lot* of stuff happens in this method, extra validation,
            processing around browser state and data, and writes to file. All of
            this makes this method slow.

            :param po_id: str, key for the page object in the POM data model
            :param cross_auth_boundary: bool, true to trigger a switch between
                                        auth and noath routing, or vice versa
            :param opts: dict, pass-through parameters for the PO's __init__()
            :return: page object for the target page
        """
        # get the previous page's name; remember that the browser has changed
        # state and we are trying to catch the page object up to the browser
        last_page = self.name  # noqa: F841

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

        # Note: page *unload* is arguably an interaction event, but we don't
        # check or log page state for that. If a particular app's page
        # transitions are difficult, revisit this.

        # assume that the PO logic is correct and accurate, and that
        # the page has completed loading
        event = f"loaded page '{po_id}'"
        self.set_event(event, page_name=new_pageobject_instance.name)

        # perform any page identity checks that are specified in the PO class
        # >> using the new page object! <<
        new_pageobject_instance.verify_self(verbose=True)

        # perform a series of file-writes
        # write the cookies to a file
        new_pageobject_instance.save_cookies(filename=event)

        # write browser metrics log to file
        new_pageobject_instance.save_browser_metrics(filename=event)

        # write browser console and peformance logs to files
        new_pageobject_instance.save_browser_logs(filename=event)

        # write webstorage to files
        new_pageobject_instance.save_webstorage(event=event, set_this_event=False)

        # generate and write accessibility logs to file
        new_pageobject_instance.save_accessibility_logs(filename=event)

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
                checks.expect_element_to_be_present(): Triggered by `True`
                    as the first value in the self.load_checks
                checks.expect_element_to_be_gone(): Triggered by `False`
                    as the first value in the self.load_checks

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
            if check[0] == True:  # noqa: E712
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
            logger.info("Writing special logs because of load errors")
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
        logger.info(f"\nAttempting to verify identity for "
                    f"'{self.name}': '{self.driver.current_url}'.")

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

    def save_cookies(self, filename=''):
        """
            Get the current page's cookies and save to a file.

            The filename can be specified by the calling code, but the
            expectation is that this is either:
            1. an event string, because the trigger for saving these cookies
               could be a page object load or reload
            2. the default of the page object's name

            :param filename: str filename for the log file;
                             defaults to PO name
            :return: None
        """
        # set the cleaned file name
        fname = filename if filename else self.name
        clean_name = utils.path_proof_name(fname)

        # get the cookies from the driver and save to the PO
        self.cookies = self.driver.get_cookies()

        utils_file.write_cookies_to_file(self.cookies, self.url,
                                         fname=clean_name)

    def save_browser_logs(self, filename=''):
        """
            Grab the Chrome driver console and network logs and write them
            to files.

            :param filename: str filename for the log file;
                             defaults to PO name
            :return:
        """
        # set the cleaned file name
        fname = filename if filename else self.name
        clean_name = utils.path_proof_name(fname)

        if pytest.custom_namespace['devtools_supported']:
            # get the logs
            performance_logs = utils_selenium.\
                get_network_traffic_logs(pageobject=self)

            console_logs = {}
            console_logs['console'] = utils_selenium.\
                get_console_logs(pageobject=self)

            logger.info("Writing special logs.")

            # write the raw performance logs to /network
            utils_file.write_network_log_to_file(log=performance_logs,
                                                 url=self.url, fname=clean_name)

            # write the scan logs to /console
            utils_file.write_console_log_to_file(log=console_logs,
                                                 url=self.url, fname=clean_name)

        else:
            logger.warning(f"Cannot access chrome logs for "
                           f"{pytest.custom_namespace['browser']}.")

    def save_browser_metrics(self, filename=''):
        """
            Grab the Chrome driver metrics log and write them to files.

            :param filename: str filename for the log file;
                             defaults to PO name
            :return:
        """
        # set the cleaned file name
        fname = filename if filename else self.name
        clean_name = utils.path_proof_name(fname)

        if pytest.custom_namespace['devtools_supported']:
            logger.info("\nWriting browser metrics logs.")
            # get the log
            metrics_log = utils_selenium.\
                get_metrics_log(pageobject=self)

            # write the raw performance logs to /network
            utils_file.write_metrics_log_to_file(log=metrics_log,
                                                 url=self.url, fname=clean_name)

        else:
            logger.warning(f"\nCannot access browser metrics logs for "
                           f"{pytest.custom_namespace['browser']}.")

    def save_webstorage(self, event, set_this_event=True):
        """
            Get the localStorage and sessionStorage for the current page (if
            available), and then write them to logfiles.

            Note: because the storage is closely tied to app state (if this
            is a React app), use the event as the base for the file name!

            Note: sometimes we don't want to call set_event() for the event
            `event`.

            :param event: str, name of the event
            :param set_this_event: bool, true to call set_event for this event
            :return: None
        """
        data = utils_selenium.get_webstorage(self)
        if set_this_event:
            self.set_event(event)
        utils_file.write_webstorage_to_files(data,
                                             current_url=self.url,
                                             pageobject_name=self.name,
                                             event=event)

    def save_accessibility_logs(self, filename=''):
        """
            Perform and save accessibility checks basd on the axe engine.

            The checks are run automatically for web pages handled
            by a welkin page object model. Results are written to the
            current test runs output/accessibility folder.

            NOTE: these checks may slow down the perceived page performance
            around page load in the context of test runs.

            TODO: refine the generated accessibility data: we really just
            want to report problems.

            The filename can be specified by the calling code, but the
            expectation is that this is either:
            1. an event string, because the trigger for running these checks
               could be a page object load or reload
            2. the default of the page object's name

            :param filename: str filename for the log file;
                             defaults to PO name
            :return: None
        """
        # instantiate axe
        axe = Axe(self.driver)

        # inject axe.core into page
        axe.inject()

        # run the axe accessibility checks
        axe_results = axe.run()
        # axe.run() caused the page to scroll to the bottom; scroll back to top
        utils_selenium.scroll_to_top_of_page(self.driver)

        # set the cleaned file name
        fname = filename if filename else self.name

        # write the results to a file
        path = pytest.custom_namespace['current test case']['accessibility folder']
        filename = f"{path}/{utils.path_proof_name(fname)}.json"
        logger.info(f"Writing accessibility logs to {filename}")
        axe.write_results(axe_results, filename)

    def set_event(self, event_name, page_name=None):
        """
            Add an event to the current page object's properties.

            An `event` is an interaction with the browser and/or site that
            MAY cause a change in page state by triggering Javascript logic
            to manipulate the DOM.

            Optionally set the name of the current page as `page_name`.
            Typically it's ok to just use the current page objects name property

            For now, we just log the fact of the event.

            :param event_name: str, name of the event
            :param page_name: str, name of page where the event occurred
            :return: None
        """
        this_event = {
            '_timestamp': time.time(),
            'event': event_name,
            'on page': page_name if page_name else self.name
        }

        logger.info(f"\nbrowser interaction event:\n{utils.plog(this_event)}")

    # #######################################
    # page object transition methods
    # #######################################
    def _click_and_load_new_page(self, element, name, po_selector,
                                 change_url=True, **actions):
        """
            Perform a click action on an element, then return a new page object
            for the page that the browser has loaded.

            The `change_url` controls the expectation of the url changing
            after this click action. This is a little bit hacky.

            Log the timestamp for the click action and save to timings.txt

            Note: Single page apps built with frameworks like React could
            make the transition between pages a little tougher to model if
            they don't change the urls for logical pages.

            :param element: webelement (for link, button, etc.)
            :param name: str, identifier for element
            :param po_selector: str, name of the target PO
            :param change_url: bool, True if url should change
            :param actions: dict, could contain key/value pairs for
                                  'pre_action' and 'post_action'
            :return next_page: page object for the next page
        """
        driver = self.driver  # minor disambiguation

        # perform the click action
        wait = WebDriverWait(driver, 20)
        if change_url:
            old_url = self.url
            logger.info(f"Old url: {old_url}")

            # some methods will insert a 'target url' key into the `actions`
            # payload, which means that a redirect is expected. If this key
            # is present, then wait for the target url to be present.
            target_url = actions.get('target url')
            logger.info(f"target url: {target_url}")
            if target_url:
                # expect a redirect
                try:
                    self._click_element(element, name, **actions)
                    wait.until(EC.url_to_be(target_url))
                    new_url = driver.current_url
                    logger.info(f"New url: {new_url}")
                except TimeoutException:
                    msg = f"URL did not change as required from '{old_url} to {target_url}'."
                    logger.error(msg)
                    logger.info(f"actual URL: {driver.current_url}")
                    self.save_screenshot(f"failed while leave {self.name}")
                    self.save_browser_logs()
                    self.save_webstorage(event=msg)
                    raise PageUnloadException(msg)

            else:
                try:
                    self._click_element(element, name, **actions)
                    wait.until(EC.url_changes(old_url))
                    new_url = driver.current_url
                    logger.info(f"New url: {new_url}")
                except TimeoutException:
                    msg = f"URL did not change as required from '{old_url}'."
                    logger.error(msg)
                    self.save_screenshot(f"failed to leave {self.name}")
                    self.save_browser_logs()
                    self.save_webstorage(event=msg)
                    raise PageUnloadException(msg)
        else:
            self._click_element(element, name, **actions)

        # load and return the PO for the next page
        logger.info(f"\nLoading page object for '{po_selector}'.")
        if actions.get('pass through to PO'):
            # In some special cases a PO's __init__() might require
            # additional args
            next_page = self.load_pageobject(po_selector, **actions)
        else:
            next_page = self.load_pageobject(po_selector)
        return next_page

    # #######################################
    # interaction event wrappers
    # #######################################
    def _goto_and_hover(self, element, name):
        """
            Set an event on moving cursor to the element `element`.

            :param element: webdriver element
            :param name: str, identifier for element
            :return: None
        """
        event = f"Cursor moved to element '{name}'"
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # TODO: verify that the hover action occurred,
        # and presumably that there was a state change
        self.set_event(event)

    def _unhover(self, x=-50, y=5):
        """
            Cancel hover by moving cursor.

            :param x: int, movement on x-axis
            :param y: int, movement on y-axis
            :return: None
        """
        event = f"unhovered: moved relative '{(x, y)}'"
        ActionChains(self.driver).move_by_offset(x, y).perform()
        self.set_event(event)

    def _click_element(self, element, name, msg=None, **actions):
        """
            Wrap the actual clicking of an element. This allows for the
            insertion of additional check points and error checking and
            handling.

            :param element: webdriver element
            :param name: str, identifier for element
            :param msg: str, optional specified event msg
            :return: None
        """
        event = f"clicked element '{name}'"
        element.click()
        self.set_event(msg if msg else event)
        if actions.get('actions'):
            if actions['actions'].get('unhover'):
                self._unhover()

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

    def _clear_field_value(self, element, name):
        """
            Wrap the clearing of an element's value. This allows for the
            insertion of additional check points and error checking and
            handling.

            :param element: webdriver element
            :param name: str, identifier for element
            :return: None
        """
        event = f"Cleared value for element '{name}'"
        element.clear()
        self.set_event(event)

    def _hard_clear_field_value(self, element, name):
        """
            Wrap the selenium utility hard_clear_input_field().

            :param element: webdriver element
            :param name: str, identifier for element
            :return element: webelement (after being cleared)
        """
        event = f"Hard cleared value for element '{name}'"
        driver = self.driver
        element = utils_selenium.hard_clear_input_field(driver, element, name)
        self.set_event(event)
        return element

    def _send_keys(self, element, name, content, msg=None):
        """
            Wrap the actual sending of keys to an element. This allows
            for the insertion of additional check points and error
            checking and handling.

            :param element: webdriver element
            :param name: str, identifier for element
            :param content: str, content to be entered into field
            :param msg: str, optional specified event msg
            :return: None
        """
        event = f"Sent content '{content}' to element '{name}'"
        element.send_keys(content)
        self.set_event(msg if msg else event)

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
                msg = f"Clicked in field '{name}'"
                self._click_element(element, name, msg)
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
                    element = self._hard_clear_field_value(element, name)
                except ControlInteractionException:
                    err_msg = f"Field '{name}' did not get cleared correctly, " \
                              f"still has value '{old_value}'"
                    logger.error(err_msg)
                    self.save_screenshot(f"{name} field not cleared")
                    raise ControlInteractionException(err_msg)

        if chunk:
            # iterate over the desired value, 1 char at a time
            # drawbacks: takes longer, adds more work
            logger.info(f"\n======> chunking input for '{name}'")
            for i, s in enumerate(content):
                self._send_keys(element, name, s)
                logger.info(f"\n======> iteration {i}: set character {s}")
                self.save_screenshot(f"{name} after set {i}")
        else:
            # everything else
            self._send_keys(element, name, content)
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
                self._send_keys(element, name, content=field_map[name])
                self.set_event(msg)
            else:
                self._unfocus_field(name)
            self.save_screenshot(f"{name} after unset")

        return True

    def _set_field_textarea(self, element, name, content, unfocus=True):
        """
            Wrap the setting of a textarea field's value.

            Note: C5 doesn't currently have field validation for text areas,
            so we can't currently negative test textareas.

            :param element: webdriver element
            :param name: str, identifier for field
            :param content: str, content to be entered in field
            :param unfocus: bool, whether to unfocus the form field;
                                  defaults to True
            :return: True
        """
        self._click_element(element, name)

        self._clear_field_value(element, name)

        self._send_keys(element, name, content)

        if unfocus:
            self._unfocus_field(name)

        return True

    def _set_field_checkbox(self, element, name, unfocus=True):
        """
            Wrap the checking/setting of a checkbox.

            NOTE: this does not handle toggling the checkbox.

            :param element: webdriver element
            :param name: str, identifier for field
            :param unfocus: bool, whether to unfocus the form field;
                                  defaults to True
            :return: True
        """
        msg = f"Clicked checkbox '{name}'"
        self._click_element(element, name, msg)

        if unfocus:
            self._unfocus_field(name)

    def _set_field_radio(self, element, name, unfocus=True):
        """
            Wrap the checking of a radio button.

            :param element: webdriver element
            :param name: str, identifier for field
            :param unfocus: bool, whether to unfocus the form field;
                                  defaults to True
            :return: True
        """
        msg = f"Clicked radio button '{name}'"
        self._click_element(element, name, msg)

        if unfocus:
            self._unfocus_field(name)

    def _set_field_file_upload(self, element, name, content, unfocus=True):
        """
            Wrap the pushing of a file's path to the input field for the
            file upload.

            NOTE: webdriver restricts the input to a string that maps
            to a local file, so we can't negative test this field.

            Note: don't click file upload fields, because that will launch
            a native OS file handler.

            :param element: webdriver element
            :param name: str, identifier for field
            :param content: str, content to be entered in field
            :param unfocus: bool, whether to unfocus the form field;
                                  defaults to True
            :return: True
        """
        msg = f"Set field '{name}' with file path '{content}'"
        self._send_keys(element, name, content, msg)

        if unfocus:
            self._unfocus_field(name)
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
