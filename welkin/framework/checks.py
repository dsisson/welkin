import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)


# #######################################
# load/unload checks
# #######################################
def expect_element_to_be_present(pageobject, check, waitfor=30):
    """
        Wait for the element specified in the check to be present; optionally
        wait for specified text to be present in that element.

        There are two version of check tuples, the 3-element tuple:
            (True, By.ID, 'search_form_input_homepage')
        and the 4-element tuple:
            (True, By.CSS_SELECTOR, 'button.foo > span', 'Submit')

        The types and meanings of the tuple elements are:
        1. bool, where True means expect the element to be present and
           False means expect the element to be gone, stale, or not displayed
        2. BY selector class and property
        3. string selector value
        4. if supplied, a string text value expected to be present in the
           element that is found with the selector. It may be more effective
           to supply an XPATH selector for the element that includes the text.

        :param pageobject: page object for the calling page
        :param check: tuple, (bool should element be present, selector method,
                              str selector))
        :param waitfor: int, wait time page load verification, defaults to
                             30 seconds
        :return: if an exception is caught, tuple of exception name + the
                                            original check tuple
    """
    name = pageobject.name
    wait = WebDriverWait(pageobject.driver, waitfor)
    try:
        if len(check) == 3:
            wait.until(EC.visibility_of_element_located(check[1:]))
            logger.info(f"\nVerified page load for '{name}': '{check[2]}' is visible.")
            return None
        else:  # 4-element check for expected text
            wait.until(EC.text_to_be_present_in_element(check[1:3], check[3]))
            logger.info(f"\nVerified page load for '{name}': '{check[3]}' is present.")
            return None

    except TimeoutException:
        msg = f"TimeoutException while attempting '{check[-1]}'"
        logger.error(msg)
        return msg, check


def expect_element_to_be_gone(pageobject, check, waitfor=30):
    """
        Wait for the element specified in the check to be gone, which may
        mean gone-gone, stale, or not visible.

        The check tuples is a 3-element tuple:
            (False, By.ID, 'search_form_input_homepage')

        The types and meanings of the tuple elements are:
        1. bool, where True means expect the element to be present and
           False means expect the element to be gone, stale, or not displayed
        2. BY selector class and property
        3. string selector value

        :param pageobject: PO for the calling page
        :param check: tuple, (bool for expected presence, selector method,
                              str selector)
        :param waitfor: int, wait time for unload verification
        :return: if check fails, tuple of exception name + check tuple
    """
    name = pageobject.name
    wait = WebDriverWait(pageobject.driver, waitfor)

    try:
        this = pageobject.driver.find_element(check[1], check[2])  # noqa: F841
        # good result!
        logger.info(f"\nUnload check '{check[1:]}' was not found.")
        try:
            wait.until_not(EC.visibility_of_element_located(check[1:]))
            logger.info(f"\nVerified page load for '{name}' with check '{check[1:]}'")
            # good result!
        except TimeoutException:
            logger.error(f"Timed out waiting for the absence of element on '{name}'")
            # because the unload check failed, we return a tuple of the str
            # exception name along with the original check tuple
            return 'TimeoutException', check

    except NoSuchElementException:
        logger.info(f"\nVerified page load for '{name}': '{check[1:]}' was not found.")
        # good result!
        return None


# #######################################
# identity checks
# #######################################
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
    if pageobject.url not in actual_url:
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
