import logging
import time
import json
import pytest

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


def get_console_logs(pageobject_instance):
    """
        Get the console for the browser, which may be empty, and write it to
        a file in output/<<testrun>>/<<testcase>>/scanlogs

        :param pageobject_instance:
        :return console_logs: list of dicts, see above example
    """
    console_logs = {}

    logger.info(f"\nGetting browser logs for page {pageobject_instance.url}.")
    console_logs['console'] = pageobject_instance.driver.get_log('browser')

    return console_logs


def get_network_traffic_logs(pageobject_instance):
    """
        Get the performance logs (aka network traffic logs) for the current
        page from the browser.

        :param pageobject_instance:
        :return jlogs: list of dicts
    """
    driver = pageobject_instance.driver
    url = pageobject_instance.url
    fname = pageobject_instance.name

    logger.info(f"\nGetting network logs for page '{fname}' at {url}.")
    raw_perflogs = driver.get_log('performance')

    # the messages are actually a string, which doesn't help as dig into
    # the logs, so we need to rewrite the network log entries as a dict
    jlogs = [{'message': json.loads(x['message']),
              'level': x['level'],
              'timestamp': x['timestamp']}
             for x in raw_perflogs]

    return jlogs
