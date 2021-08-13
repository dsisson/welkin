import logging
import time
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
        logger.info('Saved full-height screenshot: %s.' % path)
    else:
        driver.save_screenshot(path)
        logger.info('Saved screenshot: %s.' % path)
