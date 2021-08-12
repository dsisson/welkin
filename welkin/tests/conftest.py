import logging
import pytest
import time
import sys
from pathlib import Path

from welkin.framework import utils

logger = logging.getLogger(__name__)
TESTRUN_LOGFILE_NAME = 'runlog.txt'
TESTCASE_LOGFILE_NAME = 'testlog.txt'


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

    if '--help' in sys.argv:
        # If pytest is invoked with the "help" option, we don't want to
        # generate the HTML results report because that will error out.
        # Don't create any output folders or logs.
        pass
    else:
        initialize_logging()
    logger.info(f"sys.argv: {sys.argv}")


# 1.0
def pytest_configure(config):
    """
        This pytest hook happens after test collection.

        Here we are:
        + following up on the creation of output paths and logging that
          were triggered in pytest_addoption()
        + fixing the path for the pytest-html reporting plugin

        This requires that pytest.ini includes the following line so
        that there is an htmlpath attribute to modify:
            addopts = --html=output/report.html

        :param config: pytest Config object
        :return: None
    """
    add_opts_to_namespace(config)

    # update the pytest-html path to include the timestamped folder
    corrected_report_path = str(correct_results_report_path())
    pytest.welkin_namespace['htmlpath'] = corrected_report_path
    # Note: the pytest-html plugin relies on config.option.htmlpath.
    # So, even though the testrun-specific path is in the namespace,
    # we need to push that path back into the config object.
    config.option.htmlpath = corrected_report_path


# 2.0
def pytest_sessionstart(session):
    """
        Set up the test run.
        
        Use configure_pytest_sessio() for any global test session and 
        fixture logic.

        :param session: pytest request object (which is the context 
                        of the calling text method)
        :return: None
    """
    logger.info(f"{'-' * 10}")
    # the following line outputs some interesting info for debugging test runs
    # logging.info(f"session.__dict__:\n{utils.plog(session.__dict__)}")


# 3.0
def pytest_collection_modifyitems(items):
    """
        A pytest hook called after test collection used to modify or
        reorder test items.

        :param items: list, list of test item objects
        :return: None
    """
    logger.info(f"no actions taken.")


# 4.0
def pytest_collection_finish(session):
    """
        A pytest hook called after test collection has finished; we now know
        what tests will be run.

        1. Create a data model for these tests, which will look like:
            {
                "test_driver": {"short_name": "3_driver"},
                "test_first": {"short_name": "1_first"},
            }

        2. generate and store the output folder name for this test case in
        the format <<number>>_<<test case name minus the "test">>_<<tier>>,
        which will look something like this:
            1_something[some param]_test

        :param session: pytest Session object
        :return: None
    """
    logger.info(f"\n\n{'#' * 30}\n\n")
    # create container for info about the collected tests
    collected_tests = {}

    # create a container for fixtures called by these tests
    referenced_fixtures = []

    apps = set()
    collection_items = session.__dict__['items']
    for num, item in enumerate(collection_items, start=1):
        # set up for test case folder creation
        try:
            test_name = item.__dict__['name']
        except KeyError:
            test_name = item.name
        short_name = f"{num}_{test_name[5:]}"
        collected_tests[test_name] = {'short_name': short_name}

        # gather the fixtures
        referenced_fixtures = item.__dict__['_fixtureinfo'].names_closure
        for item in referenced_fixtures:
            apps.add(item)

    # add the collected test info into the welkin namespace
    pytest.welkin_namespace['collected_tests'] = collected_tests
    logger.info(f"\n\n##########################\n\n")


# 5.0
def pytest_runtestloop(session):
    """
        A pytest hook called before the tests.
    """
    pass


# 6.0
def pytest_runtest_protocol(item, nextitem):
    """
        A pytest hook called before the tests.
    """
    pass


# 7.0
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """
        A pytest hook run before the test is executed.

        :param item: a test method.
        :return: None
    """
    logger.info(f"### Set up for test {item.name} ###")
    this_test = pytest.welkin_namespace['collected_tests'][item.name]

    short_name = utils.path_proof_name(this_test['short_name'])
    testrun_path = pytest.welkin_namespace['testrun_output_path_object']
    root_log_path = pytest.welkin_namespace['testrun_output_path_object'] / TESTRUN_LOGFILE_NAME

    # create the output folder for this test case
    folder_path = utils.create_testrun_subfolder(testrun_path, short_name)

    # set up the appropriate sub-folders and special log files for this test case
    fixturenames = item.fixturenames
    set_up_testcase_reporting(folder_path, fixturenames)

    # set up global namespace path-to-this-testcase value
    pytest.welkin_namespace['this_test'] = folder_path
    logger.warning(f"### Changing log output path to the test case path. ###\n\n")

    # change the log file
    path_to_logfile = str(folder_path / TESTCASE_LOGFILE_NAME)
    logger.info(f"\n{'#' * 30}\n=====>> Testcase {item.name} logged to {path_to_logfile}\n{'#' * 30}\n\n")
    log_kwargs = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)s::%(funcName)s() [%(levelname)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.FileHandler',
                'filename': path_to_logfile,
                'mode': 'a',
                'formatter': 'detailed'
            },
            'foo': {
                'class': 'logging.FileHandler',
                'filename': path_to_logfile,
                'mode': 'a',
                'formatter': 'detailed'
            }
        },
        'loggers': {
            '': {  # root
                'handlers': ['foo'],
                'level': 'INFO',
                'propagate': False
            },
            'welkin.apps': {
                'handlers': ['foo'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    filename = set_logging_config(log_kwargs)
    yield


# 8.0
def pytest_runtest_teardown(item, nextitem):
    """
        A pytest hook run at test teardown.

        :param item: a test method
        :param nextitem: a test method to be run next
        :return: None
    """
    logger.info(f"### Tear down for test {item.name} ###")
    path_to_logfile = pytest.welkin_namespace['testrun_root_log']

    log_kwargs = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)s::%(funcName)s() [%(levelname)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.FileHandler',
                'filename': path_to_logfile,
                'mode': 'a',
                'formatter': 'detailed'
            },
        },
        'loggers': {
            '': {  # root
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }

    logger.info(f"### Closing test case logfile ###\n\n")
    filename = set_logging_config(log_kwargs)
    logger.info(f"### Reset logfile to {filename} ###\n\n\n")


# 9.0
def pytest_sessionfinish(session, exitstatus):
    """
        This hook is called after the whole test run finishes.
    """
    logger.info('No actions taken.')


# 10.0
def pytest_unconfigure(config):
    """
        This hook is the last pytest action, the final cleanup for
        the pytest run.

        This is where you would include logic for processing summary data.

        :param config: pytest config option
        :return: None
    """
    pass


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



# #########################################
# framework fixtures ######################
# #########################################
# 0.1
def initialize_logging():
    """
        Create the test framework's namespace in the pytest object,
        create the testrun's output folder, and start logging.

        :return: None
    """
    pytest.welkin_namespace = {}

    # set timestamp for the start of this test run;
    # this is used globally for this run
    timestamp = time.strftime('%y%m%d-%H%M%S')
    pytest.welkin_namespace['timestamp'] = timestamp

    # create the output folder for this test run
    welkin_folder, testrun_folder = utils.create_testrun_folder(timestamp)

    # save the welkin folder as a global config
    pytest.welkin_namespace['welkin_folder'] = str(welkin_folder)

    # save the output folder as a global config
    pytest.welkin_namespace['testrun_output_path_object'] = testrun_folder
    pytest.welkin_namespace['testrun_output_path'] = str(testrun_folder)

    path_to_logfile = str(testrun_folder / TESTRUN_LOGFILE_NAME)
    pytest.welkin_namespace['testrun_root_log'] = path_to_logfile

    # start logging
    log_kwargs = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)s::%(funcName)s() [%(levelname)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.FileHandler',
                'filename': path_to_logfile,
                'mode': 'a',
                'formatter': 'detailed'
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    filename = set_logging_config(log_kwargs)
    logger.info(pytest.welkin_namespace['testrun_output_path'])
    logger.info(f"\nnamespace:\n{utils.plog(pytest.welkin_namespace)}")


# 0.2
def set_logging_config(kwargs):
    """
        Configure and start the framework logging.

        :param output_path: Path object for path to testrun output folder
        :return filename: Path object for path to log file
    """
    import logging.config
    # start logging
    logging.config.dictConfig(kwargs)
    filename = kwargs['handlers']['default']['filename']
    logger.info(f"created log file at '{filename}'.")
    return filename


# 1.1
def add_opts_to_namespace(config):
    """
        Add the cli args from pytest_addoption() to the
        pytest.welkin_namespace dict.

        New addopts have to be manually added to this list; however,
        they can still be access through request.config.option.<foo>.

        This pytest.welkin_namespace dict is created in pytest_configure().

        :param config: pytest config option
        :return: None
    """
    opts = ['browser']
    for item in opts:
        pytest.welkin_namespace[item] = config.getoption(item)


# 1.2
def correct_results_report_path():
    """
        Change the path specified for the html results report to
        include the testrun's timestamp output folder.

        The report is generated by the html report plugin, and is invoked
        by the command line argument specified in pytest.ini:
        `--html=output/report.html`

        Because the pytest test run is invoked at the command line, we haven't
        determined the timestamp for the test run yet; so, we have to get the
        timestamp and modify that path to the report. This works because the
        report is generated after the test run finishes.

    :return new_path: Path object to the report in the testrun's folder
    """
    timestamp = pytest.welkin_namespace['timestamp']
    new_path = Path() / f"output/{timestamp}/report.html"
    logger.info(f"corrected reports path: '{new_path}'")
    return new_path


# 7.1
def set_up_testcase_reporting(path_to_subfolder, fixturenames):
    """
        Create the various output folders needed for the different
        kinds of reporting and logging (beyond the core framework log).

        :param path_to_subfolder: dict, info about the current test case
        :param fixturenames: list, string fixture names for this testcase
        :return: None
    """
    if '--collect-only' in sys.argv:
        # if pytest is invoked with the --collect-only option, don't
        # create the testrun subfolders
        msg = f"Subfolders NOT created because this testrun is collect-only."
        logger.info(msg)
    else:
        logger.info(f"fixturenames: {fixturenames}")
        output_path = path_to_subfolder

        # only create folders and logs appropriate to the app fixtures
        web_apps = []
        apis = []

        # create the requests logging folders for APIs
        if len(set(fixturenames).intersection(apis)):
            requests_folder = utils.create_testrun_subfolder(output_path, 'requests')
            pytest.welkin_namespace['testrun_requests_log_folder'] = str(requests_folder)
            logger.info(f"created folder 'requests': {pytest.welkin_namespace['testrun_requests_log_folder']}")
        else:
            logger.info(f"did NOT create 'requests' folder.")

        # create the cookies logging folder
        if len(set(fixturenames).intersection(web_apps)):
            cookie_folder = utils.create_testrun_subfolder(output_path, 'cookies')
            pytest.welkin_namespace['testrun_cookies_output'] = str(cookie_folder)
            logger.info(f"created folder 'cookies': {pytest.welkind_namespace['testrun_cookies_output']}")
        else:
            logger.info(f"did NOT create 'cookies' folder.")

        # create the screenshots logging folder
        if len(set(fixturenames).intersection(web_apps)):
            screenshots_folder = utils.create_testrun_subfolder(output_path, 'screenshots')
            pytest.welkin_namespace['testrun_screenshots_output'] = str(screenshots_folder)
            logger.info(f"created folder 'screenshots': {pytest.welkin_namespace['testrun_screenshots_output']}")
        else:
            logger.info(f"did NOT create 'screenshots' folder.")

        # create the accessibility logging folder
        if len(set(fixturenames).intersection(web_apps[1:])):
            accessibility_folder = utils.create_testrun_subfolder(output_path, 'accessibility')
            pytest.welkin_namespace['testrun_accessibility_log_folder'] = str(accessibility_folder)
            logger.info(f"created folder 'accessibility': {pytest.welkin_namespace['testrun_accessibility_log_folder']}")
        else:
            logger.info(f"did NOT create 'accessibility' folder.")

        # create the downloads folder for *every* app fixture
        # this is used by APIs, and by chromedriver for downloading files from the UI
        downloads_folder = utils.create_testrun_subfolder(output_path, 'downloads')
        pytest.welkin_namespace['testrun_downloads_log_folder'] = str(downloads_folder)
        logger.info(f"created folder 'downloads': {pytest.welkin_namespace['testrun_downloads_log_folder']}")

        # set up handling for webstorage
        if len(set(fixturenames).intersection(web_apps[3:])):  # just apps that have this
            # create the web storage logging folder
            webstorage_folder = utils.create_testrun_subfolder(output_path, 'webstorage')
            pytest.welkin_namespace['testrun_webstorage_log_folder'] = str(webstorage_folder)
            logger.info(f"created folder 'webstorage': {pytest.welkin_namespace['testrun_webstorage_log_folder']}")

            # create a container for an initial webstorage record, and initialize it
            pytest.welkin_namespace['old_webstorage'] = None
        else:
            logger.info(f"did NOT create 'webstorage' folder.")

        logger.info(f"\nnamespace:\n{utils.plog(pytest.welkin_namespace)}")
        if 'chrome' in pytest.welkin_namespace['browser']:
            # if this is a chrome browser, we can grab the chrome devtools
            # performance logging info; however, this is a CLI arg for a testrun,
            # and may not apply to every testcase in that testrun

            # create the chrome network performance folder IF this is a webapp
            if len(set(fixturenames).intersection(web_apps)):
                perflogs_folder = utils.create_testrun_subfolder(output_path, 'perflogs')
                pytest.welkin_namespace['testrun_perf_log_folder'] = str(perflogs_folder)
                logger.info(f"created folder 'perflogs': {pytest.welkin_namespace['testrun_perf_log_folder']}")
                pytest.welkin_namespace['devtools_supported'] = True
                pytest.welkin_namespace['get_perflogs'] = True
            else:
                logger.info(f"did NOT create 'perflogs' folder.")

            # create the chrome console logs folder IF this is a webapp
            if len(set(fixturenames).intersection(web_apps)):
                scanlogs_folder = utils.create_testrun_subfolder(output_path, 'scanlogs')
                pytest.welkin_namespace['testrun_scan_log_folder'] = str(scanlogs_folder)
                logger.info(f"created folder 'scanlogs': {pytest.welkin_namespace['testrun_scan_log_folder']}")
                pytest.welkin_namespace['get_scanlogs'] = True
            else:
                logger.info(f"did NOT create 'scanlogs' folder.")

        else:
            pytest.welkin_namespace['devtools_supported'] = False
            pytest.welkin_namespace['get_perflogs'] = False
            pytest.welkin_namespace['get_scanlogs'] = False


@pytest.fixture#(scope='session')
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
