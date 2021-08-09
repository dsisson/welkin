import logging
import pytest
import time
import sys
from pathlib import Path

from welkin.framework import utils

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """
        Define command line options and arguments.

        :param parser: Pytest parser object
        :return: None
    """
    parser.addoption('--browser',
                     action='store',
                     dest='browser',
                     choices=['chrome', 'headless_chrome'],
                     default='chrome',
                     help='Specify the browser to use: "chrome", "headless_chrome".')


def pytest_configure(config):
    """
        Set up the output folder, logfile, and html report file; this has
        to be done right after the command line options are parsed, because
        we need to rewrite the pytest-html path.

        This requires that pytest.ini includes the following line so
        that there is an htmlpath attribute to modify:
            addopts = --html=output/report.html

        :param config: pytest Config object
        :return: None
    """
    # set the timestamp for the start of this test run;
    # this is used globally for this run
    timestamp = time.strftime('%y%m%d-%H%M%S')
    config.timestamp = timestamp  # allow for global access

    # create the output folder for this test run
    output_path = utils.generate_output_path(timestamp)
    folder = utils.create_output_folder(output_path)

    # start logging
    filename = '%s/log.txt' % output_path
    log_format = '%(asctime)s %(name)s::%(funcName)s() [%(levelname)s] %(message)s'
    logging.basicConfig(filename=filename,
                        level=logging.INFO,
                        format=log_format)

    initial_report_path = Path(config.option.htmlpath)
    report_path_parts = list(initial_report_path.parts)

    logger.info('--------------')
    logger.info('Output folder created at "%s".' % folder)
    logger.info('Logger started and writing to "%s".' % filename)

    # insert the timestamp
    output_index = report_path_parts.index('output')
    report_path_parts.insert(output_index + 1, timestamp)

    # deal with doubled slashes
    new_report_path = Path('/'.join(report_path_parts).replace('//', '/'))

    # update the pytest-html path
    config.option.htmlpath = new_report_path
    logger.info('HTML test report will be created at "%s".' % config.option.htmlpath)
    logger.info('--------------')


@pytest.fixture(scope='session', autouse=True)
def configure_test_session(request):
    """
        Set up the test run.

        The original logic here was moved into pytest_configure(). Use configure_test_session() for any
        global test session and fixture logic.

        :param request: pytest request object (context of the calling test method)
        :return: None
    """
    logger.info('--------------')
    logger.info('request.session.__dict__: %s' % request.session.__dict__)
    # logger.info('request.config.__dict__: %s' % request.config.__dict__)
    logger.info('sys.argv: %s' % sys.argv)
    logger.info('--------------')


# @pytest.fixture(scope="function")
# def driver(request):
#     from selenium import webdriver
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(10)  # default wait for 10 seconds
#     logger.info('Starting driver.')
#     yield driver
#     driver.quit()
#     logger.info('Quiting driver.')

@pytest.fixture(scope='session')
def browser(request):
    """
        Determine the browser driver to use based on the `browser` parameter
        specified at the command line.

        The request object is introspected for the desired parameter value.

        For example:
        $ pytest tests --browser=chrome

        :param request: pytest request object
        :return: str, identifier for the appropriate browser driver
    """
    this_browser = request.config.option.browser
    logger.info('this_browser = %s' % this_browser)

    return this_browser


def base_chrome_capabilities():
    """
        Set the base desired capabilities for all chrome-derived browsers.

        :return capabilities: dict
    """
    from selenium.webdriver import DesiredCapabilities

    capabilities = DesiredCapabilities.CHROME.copy()

    # capture the devtools performance tab, which has the response headers
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    # note, there's a chrome/selenium bug in the above statement
    # so also do this the old, non-struct W3C way
    capabilities['loggingPrefs'] = {'performance': 'ALL'}
    return capabilities


def browser_chrome():
    """
        Launch the local browser, which will block other activities
        on the computer.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    #default_dir = {'download.default_directory': None#}
    # chrome_options.add_experimental_option('prefs')

    capabilities = base_chrome_capabilities()
    # this_driver = webdriver.Chrome(options=chrome_options,
    #                                desired_capabilities=capabilities)
    this_driver = webdriver.Chrome(desired_capabilities=capabilities)
    return this_driver


def browser_chrome_headless():
    """
        This allows for full-page screenshots, as well as not blocking
        use of the local computer.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    #default_dir = {'download.default_directory': None#}
    # chrome_options.add_experimental_option('prefs')

    capabilities = base_chrome_capabilities()
    this_driver = webdriver.Chrome(options=chrome_options,
                                   desired_capabilities=capabilities)

    # logger.info(f"\nbrowser options:\n{chrome_options.__dict__}")
    return this_driver


@pytest.fixture(scope="function")
def driver(request, browser):
    """
        Identify the appropriate browser driver to instantiate.

        This fixture is scoped to `function`, so it will launch and quit the driver
        for EACH calling test function.

        Call this fixture by passing the name as a parameter:
        def some_test(self, driver):
            etc.

        :param request: pytest request object (context of the calling test method)
        :param browser: str, driver identifier
        :yield driver: webdriver object
    """
    logger.info(f"Requested '{browser}' driver.")
    from selenium import webdriver
    driver = None

    if browser == 'chrome':
        driver = browser_chrome()
    elif browser == 'headless_chrome':
        driver = browser_chrome_headless()
    else:
        msg = f"Error: '{browser}' is not a valid selection."
        logger.error(msg)
        raise ValueError(msg)

    driver.set_window_size(1030, 2200)
    # implicit waits set the remote driver's properties, which may not
    # be over-rideable with explicit local waits
    # driver.implicitly_wait(10)  # default wait for 10 seconds
    user_agent = driver.execute_script("return navigator.userAgent;")

    if browser in ['chrome', 'headless_chrome']:
        # browser_version = driver.capabilities['browserVersion']
        driver_version = driver.capabilities['chrome']['chromedriverVersion']
        # logger.info(f"starting driver \n'{browser}':\nbrowser version: {browser_version}\n"
        #             f"chrome driver version: {driver_version}\n"
        #             f"useragent: '{user_agent}'\n")
        logger.info(f"starting driver \n'{browser}':\n"
                    f"chrome driver version: {driver_version}\n"
                    f"useragent: '{user_agent}'\n")
    else:
        logger.info(f"starting driver {browser}:\n"
                    f"useragent: \n'{user_agent}'")

    yield driver

    driver.quit()
    logger.info(f"Quitting '{browser}'' driver.")
