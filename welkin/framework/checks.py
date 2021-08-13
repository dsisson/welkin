import logging
from collections import namedtuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

logger = logging.getLogger(__name__)


def check_exact_url(pageobject):
    """
        Look at the entire current URL; the expected URL should match the
        actual URL. Use this if there will be no query string or the query
        string is predictable.

        :param pageobject: page object for the calling page
        :return: bool, True if the check evaluated to True, else False
    """
    actual_url = pageobject.driver.current_url
    if not pageobject.url == actual_url:
        msg = f"Url exact check: expected '{pageobject.url}', " \
              f"got '{actual_url}'."
        logger.error(msg)
        return False
    else:
        return True


def check_url(pageobject):
    """
        Look at the entire current URL and check whether the expected URL
        is contained in it. This works around unexpected or unpredictable
        string query args.

        :param pageobject: page object for the calling page
        :return: bool, True if the check evaluated to True, else False
    """
    actual_url = pageobject.driver.current_url
    if not pageobject.url in actual_url:
        msg = f"Url inclusion check: expected '{pageobject.url}' " \
              f"to be inside '{actual_url}'."
        logger.error(msg)
        return False
    else:
        return True


def check_url_chunks(pageobject):
    """
        Match a list of strings in the current URL. This method will
        perform a check for each chunk and then return a list of bool
        values corresponding to passed and failed checks.

        :param pageobject: page object for the calling page
        :return chunk_checks: list of bool check results
    """
    chunk_checks = list()
    actual_url = pageobject.driver.current_url
    for chunk in pageobject.url_chunks:
        if chunk not in actual_url:
            msg = f"Failed url chunks check: expected '{chunk}' " \
                  f"to be in '{actual_url}'."
            logger.error(msg)
            chunk_checks.append(False)
        else:
            chunk_checks.append(True)
    return chunk_checks


def check_title(pageobject):
    """
        Look at the <title> tag value and wait for it to match the
        expected title value from the page object.

        The wait is there to deal with any funkiness from SPA behavior.

        :param pageobject: page object for the calling page
        :return: bool, True if the check evaluated to True, else False
    """
    wait = WebDriverWait(pageobject.driver, 15)
    try:
        wait.until(EC.title_is(pageobject.title))
        return True
    except TimeoutException:
        logger.exception(TimeoutException)
        msg = f"Title check: expected '{pageobject.title}', " \
              f"got '{pageobject.driver.title}'."
        logger.error(msg)
        return False
