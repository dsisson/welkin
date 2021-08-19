import logging
import time
import json
import pytest

from selenium.common.exceptions import WebDriverException

from welkin.framework import utils_webstorage

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
