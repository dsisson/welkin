import logging
import time
import json
import pytest

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from welkin.framework import utils_webstorage
from welkin.framework.exceptions import ControlInteractionException

logger = logging.getLogger(__name__)


def take_and_save_screenshot(driver, filename=''):
    """
        Use the webdriver instance to generate a screenshot, then save it
        the "screenshots" folder being used for the current test run.

        :param driver: webdriver instance
        :param filename: str filename (not including the path)
        :return: None
    """
    filename = '%s_%s.png' % (time.strftime('%H%M%S'), filename.replace(' ', '_'))

    # Note: the path depends on the current test case!
    path = f"{str(pytest.welkin_namespace['testrun_screenshots_output'])}/{filename}"

    # full-screen screenshots are enabled by
    if pytest.welkin_namespace['browser'] in ['firefox', 'safari']:
        body = driver.find_element_by_tag_name('body')
        body_png = body.screenshot_as_png
        with open(path, 'wb') as file:
            file.write(body_png)
        logger.info(f"Saved full-height screenshot: {path}.")
    else:
        driver.save_screenshot(path)
        logger.info(f"Saved screenshot: {path}.")


def get_and_save_source(driver, filename=''):
    """
        Get the current page's source from the webdriver object
        and save it to the folder being used for the current test run.

        :param driver: webdriver instance
        :param filename: str, first part of filename, will be appended with timestamp;
                           defaults to empty string
        :return: None
    """
    filename = '/%s_%s.html' % (time.strftime('%H%M%S'), filename.replace(' ', '_'))

    # Note: the path depends on the current test case!
    path = f"{str(pytest.welkin_namespace['this_test'])}/{filename}"

    with open(path, 'w') as f:
        f.write(driver.page_source)
    logger.info(f"Saved page source: {path}.")


def extract_text_with_javascript(driver, element):
    """
        If a normal selenium `.text` property access on the element
        does not yield the text value, you can usually access that text
        with a direct javascript call.

        TODO: add error handling for stale element

        :param driver: webdriver instance
        :param element: webelement
        :return text: str text value for element, which may be ''
    """
    text = driver.execute_script("return arguments[0].textContent;", element)
    return text


def get_console_logs(pageobject):
    """
        Get the console for the browser, which may be empty, and write it to
        a file in output/<<testrun>>/<<testcase>>/scanlogs

        :param pageobject: page object instance
        :return console_logs: list of dicts, see above example
    """
    console_logs = {}

    logger.info(f"\nGetting browser logs for page {pageobject.url}.")
    console_logs['console'] = pageobject.driver.get_log('browser')

    return console_logs


def get_network_traffic_logs(pageobject):
    """
        Get the performance logs (aka network traffic logs) for the current
        page from the browser.

        :param pageobject: page object instance
        :return jlogs: list of dicts
    """
    driver = pageobject.driver
    url = pageobject.url
    fname = pageobject.name

    logger.info(f"\nGetting network logs for page '{fname}' at {url}.")
    raw_perflogs = driver.get_log('performance')

    # the messages are actually a string, which doesn't help as dig into
    # the logs, so we need to rewrite the network log entries as a dict
    jlogs = [{'message': json.loads(x['message']),
              'level': x['level'],
              'timestamp': x['timestamp']}
             for x in raw_perflogs]

    return jlogs


def get_webstorage(pageobject):
    """
        Wrapper to call methods to get browser local and session storage
        for the current page and convert to python dicts.

        :param pageobject: page object instance
        :return: tuple of local storage dict and session storage dict
    """
    local = get_local_storage(pageobject)
    session = get_session_storage(pageobject)
    return local, session


def get_local_storage(pageobject):
    """
        Get the window localStorage content for this browser session.

        This uses javascript called by selenium, and then has to do a bunch
        of cleanup in the returned content.

        :param pageobject: page object instance
        :return content: dict
    """
    # set the javascript logic
    script = "return { ...window.localStorage };"  # uses JS spread operator

    # run the script
    content = pageobject.driver.execute_script(script)

    # convert this dirty data into a real dict
    cleaned_content = utils_webstorage.convert_web_storage_data_to_dict(content)
    return cleaned_content


def clear_local_storage(pageobject):
    """
        Delete the local storage for this browser session.

        :param pageobject: page object instance
        :return: None
    """
    # set the javascript logic
    script = 'window.localStorage.clear();'

    # run the script
    pageobject.driver.execute_script(script)
    logger.warning(f"localStorage has been cleared")


def get_session_storage(pageobject):
    """
        Get the window sessionStorage content for this browser session.

        This uses javascript called by selenium, and then has to do a bunch
        of cleanup in the returned content.

        :param pageobject: page object instance
        :return content: dict
    """
    # set the javascript logic
    script = "return { ...window.sessionStorage };"  # uses JS spread operator
    content = None

    try:
        # run the script
        content = pageobject.driver.execute_script(script)
        # convert this dirty data into a real dict
        cleaned_content = utils_webstorage.convert_web_storage_data_to_dict(content)
        return cleaned_content
    except WebDriverException:
        # checking for storage immediately after the driver is
        # loaded will throw a WebDriverException, so ignore that
        msg = f"Ignoring a WebDriverException."
        logger.warning(msg)
        return content


def clear_session_storage(pageobject):
    """
        Delete the session storage for this browser session.

        :param pageobject: page object instance
        :return: None
    """
    # set the javascript logic
    script = 'window.sessionStorage.clear();'

    # run the script
    pageobject.driver.execute_script(script)
    logger.warning(f"sessionStorage has been cleared")


def hard_clear_input_field(pageobject, element, name):
    """
        Manually clear a text input field by backspacing over
        each character in that field's value string.

        In an app with heavy DOM manipulation and field validation,
        the DOM handling of the field's value attribute get delayed, so
        we have to get serious about removing the default value by:
        1. moving the cursor all the way to the end of the value string
           (assuming a left-to-right language like English).
        2. sending a backspace key (in a L-R language, this moves leftward
           until the strong is empty.

        :param pageobject: page object instance
        :param element: webelement
        :param name: str, name of field
        :return element: webelement (after being cleared)
    """
    driver = pageobject.driver
    logger.warning(f"getting serious about clearing the default")
    current_value = element.get_attribute('value')
    value_length = len(current_value) + 1
    logger.info(f"\nneed to unset '{current_value}'; {value_length} chars")
    # get the cursor all the way to the right
    for char in range(value_length):
        element.send_keys(Keys.RIGHT)

    latest_value = None
    while element.get_attribute('value'):
        old_value = element.get_attribute('value')
        right_char = old_value[-1]
        logger.info(f"~~~~~~~~~>> right char '{right_char}'")
        # assume that we are at the end of any value
        element.send_keys(Keys.BACKSPACE)
        event = f"backspace char '{right_char}'"
        pageobject.set_event(event)

        time.sleep(.5)  # give the browser a break, it's working hard
        # we are logging event for every backspace because
        # webstorage may get updated by javascript
        latest_value = element.get_attribute('value')
        logger.info(f"~~~~~~~~~>> value: '{latest_value}'")

    time.sleep(2)  # let the DOM catch up
    if latest_value == '':
        return element
    else:
        fname = f"{name} field not cleared"
        err_msg = f"Field '{name}' did not get cleared correctly, " \
                  f"still has value '{latest_value}'"
        logger.error(err_msg)
        take_and_save_screenshot(driver, filename=fname)
        raise ControlInteractionException(err_msg)
