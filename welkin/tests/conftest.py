import logging
import pytest
import time
import sys
from pathlib import Path

from welkin.framework import utils

logger = logging.getLogger(__name__)
# setting up the log file filenames
TESTRUN_LOGFILE_NAME = 'runlog.txt'
TESTCASE_LOGFILE_NAME = 'testlog.txt'
# hacky global counter for iterating over collected
# tests in pytest_runtest_setup()
COUNT = 1


def update_namespace(data: dict, verbose: bool = False):
    """
        Supporting method to simplify the addition of data into this
        frameworks hacky namespace solution, which is just the addition
        of a dictionary as a property on the pytest instance triggered by
        this test run invocation.

        Any change to this dict is global and will have side effects.

        :param data: dict of items to add to the namespace
        :param verbose: bool, whether to output additional logging
        :return: None
    """
    try:
        pytest.custom_namespace
    except AttributeError:
        pytest.custom_namespace = {}
        if verbose:
            logger.info(f"\nnamspace doesn't exist, so creating it")

    for k, v in data.items():
        pytest.custom_namespace[k] = v
        if verbose:
            logger.info(f"\nadded namespace '{k}': '{v}'")


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

    parser.addoption('--tier',
                     action='store',
                     dest='tier',
                     choices=['int', 'stage', 'prod'],
                     default='stage',
                     help='Specify the tier: "int", "stage", "prod".')

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
    namespace_data = {}

    # update the pytest-html path to include the timestamped folder
    corrected_report_path = str(correct_results_report_path())
    namespace_data['htmlpath'] = corrected_report_path

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)

    # Note: the pytest-html plugin relies on config.option.htmlpath.
    # So, even though the testrun-specific path is in the namespace,
    # we need to push that path back into the config object.
    config.option.htmlpath = corrected_report_path


# 2.0
def pytest_sessionstart(session):
    """
        Set up the test run.

        Use configure_pytest_session() for any global test session and
        fixture logic.

        :param session: pytest request object (which is the context
                        of the calling text method)
        :return: None
    """
    logger.info(f"{'-' * 10}")
    # the following line outputs some interesting info for debugging test runs
    # logging.info(f"\nsession.__dict__:\n{utils.plog(session.__dict__)}")


# 3.0
def pytest_collection_modifyitems(items):
    """
        A pytest hook called after test collection used to modify or
        reorder test items.

        :param items: list, list of test item objects
        :return: None
    """
    logger.info("no actions taken.")


# 4.0
def pytest_collection_finish(session):
    """
        A pytest hook called after test collection has finished; we now know
        what tests will be run.

        :param session: pytest Session object
        :return: None
    """
    logger.info("no actions taken.")
    # logger.info(f"\nsession.__dict__:\n{utils.plog(session.__dict__)}")


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

        We use this to:
        1. Create the folder to hold the logger output for the test.
           That folder is named with this syntax:
            <<number>>_<<test case name minus the "test">>_<<tier>>,
            which will look something like this:
                1_foo[some param]
                2_bar

        2. Trigger the creation of sub-folders for specific kinds of
           verbose output, depending on the types of applications being
           tested against.

           For example, if we are testing against a webapp,
           we create this kind of folder structure:
           - output (already exists)
               |- 210927-123456 (testrun folder, already exists)
                   |- 1_foo (test folder, created here)
                       |- accessibility (created here)
                       |- console (created here)
                       |- cookies (created here)
                       |- downloads (created here)
                       |- network (created here)
                       |- screenshots (created here)
                       |- webstorage (created here)

        3. Switch the logger from the root logger to the apps logger.
           This in effect moves the logging "firehose" from pointing at
           `TESTRUN_LOGFILE_NAME` to pointing at `TESTCASE_LOGFILE_NAME`.

        4. When the test case (test method) exits, the logger is
           re-pointed at the root logger.

        :param item: a test method.
        :return: None
    """
    logger.info(f"### Set up for test {item.name} ###")
    namespace_data = {}

    # extract the test method name, tweak it, and use it for
    # naming a folder in the testrun folder for the logging
    # of this current test
    try:
        test_name = item.__dict__['name']
    except KeyError:
        test_name = item.name
    short_name = f"{COUNT}_{test_name[5:]}"

    # extract the fixture names associated with this current test
    fixtures = []
    referenced_fixtures = item.__dict__['_fixtureinfo'].names_closure
    logger.info(f"\nreferenced_fixtures: {referenced_fixtures}")
    for this_fixture in referenced_fixtures:
        fixtures.append(this_fixture)
    # `COUNT` is used in the naming of the test output folder;
    # we need them to increment for each collected test
    globals()['COUNT'] += 1  # this is hacky because there is no iterator

    # create the output folder for this test case
    testrun_path = pytest.custom_namespace['testrun_output_path_object']
    folder_path = utils.create_test_output_subfolder(testrun_path, short_name)

    # set up the appropriate sub-folders and
    # special log files for this test case
    set_up_testcase_reporting(folder_path, fixtures)

    # set up global namespace path-to-this-testcase value
    namespace_data['this_test'] = folder_path
    logger.warning("### Changing log output path to the test case path. ###\n\n")

    # redirect logging from the test run logger to the test case logger
    path_to_logfile = str(folder_path / TESTCASE_LOGFILE_NAME)
    logger.info(f"\n{'#' * 30}\n=====>> Testcase {item.name} "
                f"logged to {path_to_logfile}\n{'#' * 30}\n\n")
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
    filename = set_logging_config(log_kwargs)  # noqa: F841

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)

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
    path_to_logfile = pytest.custom_namespace['testrun_root_log']

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

    logger.info("### Closing test case logfile ###\n\n")
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

        The original logic here was moved into pytest_configure().
        Use configure_test_session() for any global test session and
        fixture logic.

        :param request: pytest request object (context of the
                        calling test method)
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
    namespace_data = {}

    # set timestamp for the start of this test run;
    # this is used globally for this run
    timestamp = time.strftime('%y%m%d-%H%M%S')
    namespace_data['timestamp'] = timestamp

    # create the output folder for this test run
    welkin_folder, testrun_folder = utils.create_test_output_folder(timestamp)

    # save the welkin folder as a global config
    namespace_data['welkin_folder'] = str(welkin_folder)

    # save the output folder as a global config
    namespace_data['testrun_output_path_object'] = testrun_folder
    namespace_data['testrun_output_path'] = str(testrun_folder)

    path_to_logfile = str(testrun_folder / TESTRUN_LOGFILE_NAME)
    namespace_data['testrun_root_log'] = path_to_logfile

    # start logging; nothing that happens before this gets logged!
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
    set_logging_config(log_kwargs)

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)
    logger.info(f"\nnamespace:\n{utils.plog(pytest.custom_namespace)}")


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
        Add the CLI args from pytest_addoption() to the
        pytest.custom_namespace dict.

        New addopts have to be manually added to this list; however,
        they can still be access through request.config.option.<foo>.

        This pytest.custom_namespace dict is created in pytest_configure().

        :param config: pytest config option
        :return: None
    """
    namespace_data = {}
    opts = ['browser', 'tier']
    for item in opts:
        namespace_data[item] = config.getoption(item)

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)


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
    timestamp = pytest.custom_namespace['timestamp']
    new_path = Path() / f"output/{timestamp}/report.html"
    logger.info(f"corrected reports path: '{new_path}'")
    return new_path


# 1.3
def set_up_tier_globals(config):
    """
        The tier is specified at run time (the default is STAGE tier).
        Determine the tier-specific configuration settings and strings to use
        during testing against the specified tier.

        Of particular importance here are:
        + application models, critical for e2e testing; we need to know what
          apps are available for the current tier
        + user models, critical for e2e testing; we need to know the users
          for these apps
        + safe handling of the credentials for users
        + apps we will integrate with during the test run

        Note: this logic is in a method called by pytest_configure instead of
        in a test fixture because tests are collected *before* fixtures are
        parsed; this means that the globals set by the command line parsers
        don't get set until *after* the tests which call them are collected.

        The config object is introspected for the desired parameter value.

        The values set here are pushed into a pytest global environment
        variable called `custom_namespace`; this is available when you import
        pytest into a module. This namespace is now set in initialize_logging().

        Context example example:
        $ pytest tests --tier=stage

        Some general values can be accessed directly:
        >>> pytest.custom_namespace['tier']
        stage

        :param config: pytest config object
        :return: None
    """
    namespace_data = {}
    this_tier = config.option.tier
    namespace_data['tier'] = this_tier
    logger.info(f"this_tier: '{this_tier}'.")

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)

    return None


@pytest.fixture(scope='session')
def auth():
    """
        Fixture that calls the fixture that manages passwords via a
        key store on a cloud service; the intent is to simplify changes
        AND to have a simple fixture name that is not tied to a service
        name. This fixture name will be used as an arg in test methods,
        and it would suck to replace that.

        :return aws_session: AWS session object
    """
    # we currently use aws for managing test user account passwords
    logger.info("\n\n=======> called auth()")
    return aws()


# 7.1
def set_up_testcase_reporting(path_to_subfolder, fixturenames):
    """
        For every specific test instance being run, create the various output
        folders needed for the different kinds of reporting and logging (beyond
        the core framework log). Depending on the "types" of apps being pulled
        into the test instance (via fixtures), different kinds of data will
        be logged or saved, so create the folders appropriate to this test's
        apps.

        :param path_to_subfolder: dict, info about the current test case
        :param fixturenames: list, string fixture names for this testcase
        :return: None
    """
    if '--collect-only' in sys.argv:
        # if pytest is invoked with the --collect-only option, don't
        # create the testrun subfolders
        msg = "Subfolders NOT created because this testrun is collect-only."
        logger.info(msg)
    else:
        logger.info(f"fixturenames: {fixturenames}")
        output_path = path_to_subfolder
        namespace_data = {}

        # #############################################
        # after you add an app fixture to conftest.py, you must add
        # the str name for that app fixture to the appropriate list
        # below. This allows you to use that app fixture as a test
        # method argument and have the appropriate folders and
        # logging in place.
        # #############################################
        integrations = ['auth']  # not used, but helps with context  # noqa: F841
        web_apps = ['duckduckgo']
        apis = ['colourlovers', 'dadjokes', 'genderizer']

        # only create folders and logs appropriate to the app fixtures
        is_api = len(set(fixturenames).intersection(apis))
        is_webapp = len(set(fixturenames).intersection(web_apps))
        logger.info(f"\napp types: is_api {is_api}; is_webapp: {is_webapp}")

        # always create the integrations logging folder, for any test instance
        folder_type = 'integrations'
        requests_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
        namespace_data[f"testrun_{folder_type}_log_folder"] = requests_folder
        logger.info(f"created folder '{folder_type}': {requests_folder}")

        # create the requests logging folders for APIs
        folder_type = 'requests'
        if is_api:
            requests_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = requests_folder
            logger.info(f"created folder '{folder_type}': {requests_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        # create the cookies logging folder for webapps
        folder_type = 'cookies'
        if is_webapp:
            cookie_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_output"] = cookie_folder
            logger.info(f"created folder '{folder_type}': {cookie_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        # create the screenshots logging folder for webapps
        folder_type = 'screenshots'
        if is_webapp:
            screenshots_folder = \
                str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_output"] = screenshots_folder
            logger.info(f"created folder '{folder_type}': {screenshots_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        # create the accessibility logging folder for webapps
        folder_type = 'accessibility'
        if is_webapp:
            accessibility_folder = \
                str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = accessibility_folder
            logger.info(f"created folder '{folder_type}': {accessibility_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        # create the downloads folder for apis AND webapps
        # this is used by APIs,
        # and by chromedriver for downloading files from the UI
        folder_type = 'downloads'
        if is_api or is_webapp:
            downloads_folder = \
                str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = downloads_folder
            logger.info(f"created folder '{folder_type}': {downloads_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        # set up handling for web storage for webapps
        folder_type = 'webstorage'
        if is_webapp:
            webstorage_folder = \
                str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = webstorage_folder
            logger.info(f"created folder '{folder_type}': {webstorage_folder}")
        else:
            logger.info(f"did NOT create '{folder_type}' folder")

        logger.info(f"\nnamespace:\n{utils.plog(pytest.custom_namespace)}")

        is_chrome = 'chrome' in pytest.custom_namespace['browser']
        if is_chrome and is_webapp:
            # if this is a chrome browser, we can grab the chrome devtools
            # performance logging info; however, this is a CLI arg for a testrun,
            # and may not apply to every testcase in that testrun

            # create the chrome network performance folder (for all right now)
            folder_type = 'network'
            network_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = network_folder
            logger.info(f"created folder '{folder_type}': {network_folder}")
            namespace_data['devtools_supported'] = True
            namespace_data['get_network'] = True

            # create the chrome console logs folder (for all right now)
            folder_type = 'console'
            console_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = console_folder
            logger.info(f"created folder '{folder_type}': {console_folder}")
            namespace_data['get_console'] = True

            # create the browser metrics logs folder (for all right now)
            folder_type = 'metrics'
            metrics_folder = str(utils.create_test_output_subfolder(output_path, folder_type))
            namespace_data[f"testrun_{folder_type}_log_folder"] = metrics_folder
            logger.info(f"created folder '{folder_type}': {console_folder}")
            namespace_data['get_metrics'] = True

        else:
            logger.info("did NOT create 'network' folder")
            logger.info("did NOT create 'console' folder")
            logger.info("did NOT create 'metrics' folder")
            namespace_data['devtools_supported'] = False
            namespace_data['get_network'] = False
            namespace_data['get_console'] = False
            namespace_data['get_metrics'] = False

        # update our hacky namespace
        update_namespace(namespace_data, verbose=True)


@pytest.fixture
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
        Set the base options for all chrome-derived browsers.

        :return capabilities: dict
    """
    from selenium.webdriver.chrome.options import Options

    options = Options()
    # enable collection of network logging
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    return options


def browser_chrome():
    """
        Launch the local browser, which will block other activities
        on the computer.
    """
    from selenium import webdriver

    options = base_chrome_capabilities()
    this_driver = webdriver.Chrome(options=options)
    return this_driver


def browser_chrome_headless():
    """
        This allows for full-page screenshots, as well as not blocking
        use of the local computer.
    """
    from selenium import webdriver

    options = base_chrome_capabilities()
    options.add_argument('--headless')
    this_driver = webdriver.Chrome(options=options)
    logger.info(f"\nbrowser options:\n{utils.plog(options.__dict__)}")
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
    # enable collection of performance metrics
    driver.execute_cdp_cmd('Performance.enable', {})

    if browser in ['chrome', 'headless_chrome']:
        driver_version = driver.capabilities['chrome']['chromedriverVersion']
        logger.info(f"starting driver \n'{browser}':\n"
                    f"chrome driver version: {driver_version}\n"
                    f"useragent: '{user_agent}'\n")
    else:
        logger.info(f"starting driver {browser}:\n"
                    f"useragent: \n'{user_agent}'")

    yield driver

    driver.quit()
    logger.info(f"Quitting '{browser}' driver.")


# #########################################
# integration/SDK fixtures: if you add it here,
# you must also add a corresponding wrapper to:
# 1. integrations/
# 2. conftest.py::set_up_testcase_reporting()
# NOTE: not decorated as a fixture!
# #########################################
def aws():
    """
        Fixture that creates an AWS session and returns that to the
        calling test; this only executes if a collected test calls
        this fixture.

        A better name would be "get_aws_session_as_precursor_to_get_password",
        but fixture names have to be short and reasonably clear.

        The intent here is to create a single AWS session, and have each test
        create its own AWS client and then get the password.

        :return aws_session: AWS session object
    """
    logger.info("\n\n=======> called aws()")
    from welkin.integrations.aws.aws import AWSSession
    # create a session object tied to the local default config
    # for region and IAM user
    aws_session = AWSSession(verbose=True)
    logger.info(f"\n--> AWS session {aws_session} ({id(aws_session)})")
    return aws_session


# #########################################
# app fixtures: if you add it here, you must
# also add it to:
# 1. conftest.py::set_up_testcase_reporting()
# 2. data/applications.py
# #########################################
@pytest.fixture(scope='session')
def duckduckgo(request):
    """
        This test fixture is a trigger for setting up authentication
        management for the duckduckgo app.

        Note: not really, this is just an example to use for real apps
        that have actual users with real credentials in AWS.
    """
    pass


@pytest.fixture(scope='session')
def colourlovers(request):
    """
        This test fixture is a trigger for setting up authentication
        management for the colourlovers api.

        Note: not really, this is just an example to use for real apps
        that have actual users with real credentials in AWS.
    """
    pass


@pytest.fixture(scope='session')
def dadjokes(request):
    """
        This test fixture is a trigger for setting up authentication
        management for the dadjokes api.

        Note: not really, this is just an example to use for real apps
        that have actual users with real credentials in AWS.
    """
    pass


@pytest.fixture(scope='session')
def genderizer(request):
    """
        This test fixture is a trigger for setting up authentication
        management for the genderizer api.

        Note: not really, this is just an example to use for real apps
        that have actual users with real credentials in AWS.
    """
    pass
