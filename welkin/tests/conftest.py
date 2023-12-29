import logging
import pytest
import time
import sys
import os
from pathlib import Path

from applitools.selenium import *

from welkin.framework import utils

logger = logging.getLogger(__name__)

# setting up folders and log files
FRAMEWORK = 'welkin'
TESTRUN_LOGFILE_NAME = 'runlog.txt'
TESTCASE_LOGFILE_NAME = 'testlog.txt'
TESTRUN_HTML_REPORT = 'report.html'
# hacky global counter for iterating over collected
# tests in pytest_runtest_setup()
COUNT = 1


def update_namespace(data: dict, verbose: bool = False):
    """
        Supporting method to simplify the addition of data into this
        framework's hacky namespace solution, which is just the addition
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
            logger.info('\nnamespace doesn\'t exist, so creating it')

    for key, value in data.items():
        # sometimes we feed in a value that's a dict, so handle nesting
        if isinstance(value, dict):
            for k, v in data[key].items():
                # update the hacky namespace object
                pytest.custom_namespace[key] = {k: value}
                if verbose:
                    logger.info(f"\nadded namespace '{k}': '{v}'")
        # update the hacky namespace object
        pytest.custom_namespace[key] = value
        if verbose:
            logger.info(f"\nadded namespace '{key}': '{value}'")


def pytest_addoption(parser):
    """
        Define command line options and arguments.

        Options here should be synced with the list of important options
        in pytest_configure(), so that get written to the hacky custom
        namespace.

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

    parser.addoption('--ultrafast_grid',
                     action='store',
                     dest='applitools_ultrafast_grid',
                     choices=['yes', 'no'],
                     default='no',
                     help='Use Applitools ultra fast execution grid? "yes" or "no"')

    parser.addoption('--execution_cloud',
                     action='store',
                     dest='applitools_execution_cloud',
                     choices=['yes', 'no'],
                     default='no',
                     help='Use Applitools execution cloud? "yes" or "no"')


# 1.0
def pytest_configure(config):
    """
        This pytest hook happens BEFORE test collection.

        1. Here we are calling initialize_logging(), which:
            + triggers the creation of output folders
            + enables logging
            + dynamically re-writes the output path used by the
              pytest-html reports plugin

            This requires that pytest.ini includes the following line so
            that there is a htmlpath attribute to modify:
                addopts = --html=output/report.html

        2. extracting important options and adding them to the
          custom namespace

        :param config: pytest Config object
        :return: None
    """
    initialize_logging(config)
    logger.info(f"sys.argv: {sys.argv}")

    # extract the values of the following sys.args options
    # and push them into the namespace
    namespace_data = {}
    opts = ['browser', 'tier']
    for item in opts:
        namespace_data[item] = config.getoption(item)

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)

    # based on the browser, also set a devtools flag that
    # will control the creation of some output folders; we need to
    # not add folders for unsupported browser info methods
    if config.getoption('browser') in ['chrome', 'headless_chrome']:
        update_namespace({'devtools_supported': True}, verbose=True)
    else:
        update_namespace({'devtools_supported': False}, verbose=True)

    # check for commands to run on Applitools grid or execution cloud,
    # because we need know to know that immediately
    applitools_run_config(config)


# 2.0
def pytest_sessionstart(session):
    """
        Set up the test run, but before any collection.

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

        We are using this to identify whether we are using Applitools,
        and if we are, then we:
        1. create an output folder for any Applitools SDK logging
        2. trigger the redirection from the default logging target
           to our specified folder

        :param items: list, test item objects
        :return: None
    """
    # get the set of all test fixture names
    fixtures = set()
    for item in items:
        fixtures.update(item.__dict__['fixturenames'])

    # if the `eyes` fixture is present, that tells us that the SDK
    # will be used, so we need to hijack the log output
    if 'eyes' in fixtures:
        run_folder = pytest.custom_namespace['testrun paths']['folder']
        applitools_path = redirect_applitools_logging(run_folder)
        paths = {'applitools log path': applitools_path}
        update_namespace(paths, verbose=True)
        logger.info('\nApplitools: `eyes` fixture found, so creating folder.')


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
    logger.info(f"\n### Set up for test {item.name} ###")
    namespace_data = {}

    # extract the test method name, tweak it, and use it for
    # naming a folder in the testrun folder for the logging
    # of this current test
    try:
        test_name = item.__dict__['name']
    except KeyError:
        test_name = item.name
    # insert COUNT so that the folders sort by collection order
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
    test_run_path = pytest.custom_namespace['testrun paths']['folder']
    testcase_folder_path = test_run_path / short_name
    create_test_output_subfolder(testcase_folder_path)

    # set up the appropriate sub-folders and
    # special log files for this test case
    set_up_testcase_reporting(testcase_folder_path, fixtures)

    # set up global namespace path-to-this-testcase value
    namespace_data['this_test'] = testcase_folder_path
    logger.warning("\n### Changing log output path to the test case path. ###\n\n")

    # redirect logging from the test run logger to the test case logger
    path_to_logfile = str(testcase_folder_path / TESTCASE_LOGFILE_NAME)
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
            f"{FRAMEWORK}.apps": {
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

        Point the logger from the test case back to the test run context.

        :param item: a collected test method
        :param nextitem: a test method to be run next
        :return: None
    """
    logger.info(f"\n### Tear down for test {item.name} ###")
    path_to_logfile = pytest.custom_namespace['testrun paths']['logfile']

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

    logger.info('\n### Closing test case logfile ###\n\n')
    filename = set_logging_config(log_kwargs)
    logger.info(f"\n### Reset logfile to {filename} ###\n\n\n")


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

        :param config: pytest config object
        :return: None
    """
    pass


@pytest.fixture(scope='session', autouse=True)
def configure_test_session(request):
    """
        Set up the test run.

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
def set_logging_config(kwargs):
    """
        Configure and start the framework logging.

        :param kwargs: dict, logger config arguments
        :return filename: Path object for path to log file
    """
    import logging.config
    # start logging
    logging.config.dictConfig(kwargs)
    filename = kwargs['handlers']['default']['filename']
    logger.info(f"\ncreated log file at '{filename}'.")
    return filename


# 1.1
def initialize_logging(config):
    """
        Create the test framework's namespace in the pytest object,
        create the testrun's output folder, and start logging.

        :param config: pytest config object
        :return: None
    """
    namespace_data = {}

    # set timestamp for the start of this test run;
    # this is used globally for this run
    timestamp = time.strftime('%y%m%d-%H%M%S')
    namespace_data['timestamp'] = timestamp

    # update our hacky namespace
    update_namespace(namespace_data, verbose=True)

    # create the output folder for this test run
    framework_folder, testrun_folder = create_run_output_folder(timestamp)
    path_to_logfile = str(testrun_folder / TESTRUN_LOGFILE_NAME)

    # Change the path specified for the html test results report to include
    # the testrun's timestamp output folder. The report is generated by the
    # pytest-html report plugin, and is invoked by the command line argument
    # specified in pytest.ini: `--html=output/report.html`
    htmlreport_path = testrun_folder / TESTRUN_HTML_REPORT

    # Note: the pytest-html plugin relies on config.option.htmlpath.
    # So, even though the testrun-specific path is in the namespace,
    # we need to push that path back into the config object.
    html_path = str(htmlreport_path)
    config.option.htmlpath = html_path

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

    # create test run paths for namespace
    paths = {'testrun paths': {
                'folder': testrun_folder,
                'logfile': testrun_folder / TESTRUN_LOGFILE_NAME,
                'html report': htmlreport_path
    }}
    # update our hacky namespace
    logging.info('\n--> setting paths in namespace')
    update_namespace(paths, verbose=True)

    # set up test case namespacing
    update_namespace({'test cases': {}})

    logger.info(f"\nnamespace:\n{utils.plog(pytest.custom_namespace)}")


def redirect_applitools_logging(testrun_folder):
    """
        Create the Applitools logging folder. By default, this is in a local
        folder that is NOT useful for our test logging. The file name is auto-
        generated by the Applitools SDK.

        :param testrun_folder: PosixPath instance of run folder
        :return applitools_log_path_for_this_testrun: PosixPath instance of log folder
    """
    applitools_log_path_for_this_testrun = testrun_folder / 'applitools'
    os.environ['APPLITOOLS_LOG_DIR'] = str(applitools_log_path_for_this_testrun)
    logger.info(f"\napplitools log path for testrun: {applitools_log_path_for_this_testrun}")
    return applitools_log_path_for_this_testrun


# 1.1.1
def create_run_output_folder(timestamped_name):
    """
        Every pytest invocation triggers a bunch of logging actions. During
        the pytest start up routines, logging is enabled and configured,
        including the creation of timestamped folders for the output, which is
        managed below.

        :param timestamped_name: str
        :return: PosixPath tuple, framework_root_path & testrun_path
    """
    # Get the absolute path to the current local directory.
    # This Path object will look like
    # PosixPath('/Users/<<name>>/dev/framework/framework')
    base_path = Path.cwd()

    # Get the path parts up to and including the first instance of `framework`.
    # We can't be certain that we are in the correct directory for running
    # framework, so focus on the first "framework" instance and build from there.
    parts = base_path.parts[:base_path.parts.index(FRAMEWORK) + 1]

    # generate the path to the output folder
    framework_root_path = Path('/').joinpath(*list(parts)) / FRAMEWORK
    output_path = Path('/').joinpath(*list(parts)) / f"{FRAMEWORK}/output"
    testrun_path = output_path / timestamped_name

    # create the output path if it doesn't exist
    if not output_path.exists():
        output_path.mkdir()

    # create the testrun folder (it won't already exist)
    if not testrun_path.exists():
        testrun_path.mkdir()

    return framework_root_path, testrun_path


# 7.1
def create_test_output_subfolder(path):
    """
        Create a folder `folder` at path `path`.

        :param path: Path path to the requested folder
        :return: None
    """
    if not path.exists():
        path.mkdir()
        logger.info(f"\nCreated sub-folder: {str(path)}")
    else:
        logger.info("\nSub-folder already exists.")


# 7.2
def set_up_testcase_reporting(testcase_folder, fixturenames):
    """
        For every specific test instance being run, create the various output
        folders needed for the different kinds of reporting and logging (beyond
        the core framework log). Depending on the "types" of apps being pulled
        into the test instance (via fixtures), different kinds of data will
        be logged or saved, so create the folders appropriate to this test's
        apps.

        :param testcase_folder: Path, path to the current test case's folder
        :param fixturenames: list, string fixture names for this testcase
        :return: None
    """
    if '--collect-only' in sys.argv:
        # if pytest is invoked with the --collect-only option, don't
        # create the testrun subfolders
        msg = "Subfolders NOT created because this testrun is collect-only."
        logger.info(msg)
    else:
        logger.info(f"\nfixturenames: {fixturenames}")
        logger.info(f"\ntestcase_folder: {testcase_folder}")
        testcase = testcase_folder.parts[-1]

        # #############################################
        # after you add an app fixture to conftest.py, you must add
        # the str name for that app fixture to the appropriate list
        # below. This allows you to use that app fixture as a test
        # method argument and have the appropriate folders and
        # logging in place.
        # #############################################
        integrations = ['auth']  # not used, but helps with context  # noqa: F841
        drivers = ['driver']
        web_apps = ['duckduckgo', 'sweetshop']
        apis = ['colourlovers', 'dadjokes', 'genderizer']

        # set up config for folder requirements
        required_folders = {
            'api': ['requests'],
            'driver': ['driver'],  # browser/driver logging
            'web_app': ['cookies',  # cookies
                        'screenshots',  # screenshots from POM and tests, etc.
                        'accessibility',  # reports generated by POM for every page
                        'webstorage'  # local and session
                        ]
        }

        # only create folders and logs appropriate to the app fixtures
        is_api = len(set(fixturenames).intersection(apis))
        is_driver = len(set(fixturenames).intersection(drivers))
        is_webapp = len(set(fixturenames).intersection(web_apps))
        logger.info(f"\napp types: is_api {is_api}; is_webapp: {is_webapp}")

        # some folders are common to all
        folders_to_create = ['integrations', 'downloads']
        if is_api:
            folders_to_create.extend(required_folders['api'])
        if is_driver:
            folders_to_create.extend(required_folders['driver'])
        if is_webapp:
            folders_to_create.extend(required_folders['web_app'])
            if pytest.custom_namespace.get('devtools_supported'):
                # some capabilities are currently restricted to Chrome browsers
                folders_to_create.extend(['network', 'console', 'metrics'])

        # #############################################
        # For the current test case, create the relevant child folders
        # to which various logging and output will be written.
        # Note: This mechanism relies on side effects! Specifically,
        # various framework write methods pull paths from the custom
        # namespace, and those paths are overwritten here in
        # set_up_testcase_reporting(). This will be a problem
        # if we attempt to parallelize the execution of the
        # collected tests.
        # #############################################
        paths = {testcase: {}}  # set up individual test case namespace
        current_testcase = {'current test case': {'name': testcase}}
        for folder in folders_to_create:
            this_folder_path = testcase_folder / folder
            create_test_output_subfolder(this_folder_path)
            logger.info(f"\ncreated folder '{folder}': {this_folder_path}")

            # update local data model
            paths[testcase][f"{folder} folder"] = this_folder_path

        # manually *add* (not overwrite) this test case info to the namespace
        pytest.custom_namespace['test cases'].update(paths)

        # overwrite the namespace entry for 'current test case'
        current_testcase['current test case'].update(paths[testcase])
        update_namespace(current_testcase, verbose=True)

        logger.info(f"\nnamespace after test folder creation:"
                    f"\n{utils.plog(pytest.custom_namespace)}")


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
    logger.info('\nthis_browser: %s' % this_browser)
    return this_browser


def base_chrome_capabilities(webdriver):
    """
        Set the base options for all chrome-derived browsers.

        see https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md

        :param webdriver: webdriver package
        :return options: options object
    """
    options = webdriver.ChromeOptions()

    # set basic options to improve behavior for testing
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-features=Translate')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--ash-no-nudges')
    options.add_argument('--disable-search-engine-choice-screen')

    # enable collection of network logging
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    return options


def base_chrome_services(webdriver):
    """
        Set the Chrome service to write the browser/driver log tp
        the test case's `driver` folder file.

        see https://www.selenium.dev/documentation/webdriver/browsers/chrome/

        :param webdriver: webdriver package
        :return service: Chrome service object
    """
    # get path to driver log; this is a PosixPath object
    folder = pytest.custom_namespace['current test case']['driver folder']

    # set the file output & cast to a string
    log_path = str(folder / 'driver.txt')
    logger.info(f"\ndriver log path: {log_path}")

    # set the service arguments for logging
    args = ['--append-log',
            '--readable-timestamp',
            '--log-level=INFO']

    # set the service output configuration
    service = webdriver.ChromeService(service_args=args,
                                      log_output=log_path)
    return service


def browser_chrome():
    """
        Launch the local browser, which will block other activities
        on the computer unless using headless.

        This uses selenium webdriver manager, new with selenium 4.*.

        :return this_driver: configured Chrome browser driver
    """
    from selenium import webdriver

    service = base_chrome_services(webdriver)
    logger.info(f"\nbrowser services:\n{utils.plog(service.__dict__)}")

    options = base_chrome_capabilities(webdriver)
    logger.info(f"\nbrowser options:\n{utils.plog(options.__dict__)}")

    this_driver = webdriver.Chrome(service=service, options=options)
    return this_driver


def browser_chrome_headless():
    """
        This allows for full-page screenshots, as well as not blocking
        use of the local computer.

        :return this_driver: configured Chrome headless-browser driver
    """
    from selenium import webdriver

    service = base_chrome_services(webdriver)
    logger.info(f"\nbrowser services:\n{utils.plog(service.__dict__)}")

    options = base_chrome_capabilities(webdriver)
    options.add_argument('--headless=new')
    logger.info(f"\nbrowser options:\n{utils.plog(options.__dict__)}")

    this_driver = webdriver.Chrome(service=service, options=options)
    return this_driver


@pytest.fixture(scope="function")
def driver(request, browser):
    """
        Identify the appropriate browser driver to instantiate.

        This fixture is scoped to `function`, so it will launch and quit the driver
        for EACH calling test function.

        If using Applitools Execution Cloud, we must have:
            1. permission for access from Applitools
            2. an account and a valid API key
            3. the Applitools SDK for python

        Note: if we want to test local websites with no public URL with
        Applitools execution cloud, we can do this with a secured tunnel; see:
        https://applitools.com/docs/topics/execution-cloud/setup.html

        Call this fixture by passing the name as a parameter:
        def some_test(self, driver):
            etc.

        :param request: pytest request object (context of the calling test method)
        :param browser: str, driver identifier
        :yield driver: webdriver object
    """
    logger.info(f"\nRequested '{browser}' driver.")
    driver = None

    # applitools setup flags
    use_execution_cloud = None
    if pytest.custom_namespace.get('applitools'):
        if pytest.custom_namespace['applitools'].get('use execution cloud'):
            use_execution_cloud = True

    # #############################################################
    # Run on applitools execution cloud with visual testing
    # #############################################################
    logger.info(f"\n---> namespace for applitools: "
                f"\n{utils.plog(pytest.custom_namespace)}")

    if use_execution_cloud:
        # This means that tests will be run on the Applitools Execution cloud
        from selenium import webdriver
        options = base_chrome_capabilities(webdriver)
        logger.info(f"\nbrowser options:\n{utils.plog(options.__dict__)}")

        driver = webdriver.Remote(
            command_executor=Eyes.get_execution_cloud_url(),
            options=options)
        yield driver
        driver.quit()
        logger.info(f"Quitting 'applitools' & '{browser}' driver.")

    # #############################################################
    # Run locally with Chrome browser
    # #############################################################
    elif browser in ['chrome', 'headless_chrome']:
        if browser == 'chrome':
            driver = browser_chrome()
        elif browser == 'headless_chrome':
            driver = browser_chrome_headless()

        driver_version = driver.capabilities['chrome']['chromedriverVersion']
        logger.info(f"\nstarting driver \n'{browser}':"
                    f"\nchrome driver version: {driver_version}\n")

        # set the default window dimensions; can be over-ridden at the POM layer
        driver.set_window_size(1030, 2200)
        # implicit waits set the remote driver's properties, which may not
        # be over-rideable with explicit local waits
        # driver.implicitly_wait(10)  # default wait for 10 seconds
        user_agent = driver.execute_script("return navigator.userAgent;")
        logger.info(f"\nuseragent: \n'{user_agent}'")

        # enable collection of performance metrics
        driver.execute_cdp_cmd('Performance.enable', {})

        yield driver
        driver.quit()
        logger.info(f"Quitting '{browser}' driver.")

    # #############################################################
    # ERROR out
    # #############################################################
    else:
        msg = f"Error: '{browser}' is not a valid selection."
        logger.error(msg)
        raise ValueError(msg)


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


# #########################################
# Applitools fixtures
# NOTE: decorated as fixtures!
# #########################################
@pytest.fixture(scope='session')
def applitools_key():
    """
        Reads the Applitools API key from the APPLITOOLS_API_KEY environment
        variable.

        This is stored locally in .bash_profile.

        :return: str key
    """
    key = os.getenv('APPLITOOLS_API_KEY')
    return key


def applitools_run_config(config):
    """
        Convert CLI arg values to bool values and return as tuple.

        example:
            >>> grid, cloud = applitools_run_config()

        :param request: pytest request object
        :return: tuple(applitools_ultrafast_grid, applitools_execution_cloud)
    """
    logger.info(f"\n---> namespace for applitools config: "
                f"\n{utils.plog(pytest.custom_namespace)}")
    use_grid = config.option.applitools_ultrafast_grid
    logger.info('\nuse_grid: %s' % use_grid)
    applitools_ultrafast_grid = True if use_grid == 'yes' else False

    use_cloud = config.option.applitools_execution_cloud
    logger.info('\nexecution_cloud: %s' % use_cloud)
    applitools_execution_cloud = True if use_cloud == 'yes' else False

    settings = {
        'applitools': {
            'use ultrafast grid': applitools_ultrafast_grid,
            'use execution cloud': applitools_execution_cloud
        }}
    update_namespace(settings, verbose=True)

    logger.info(f"\napplitools namespace:\n{utils.plog(pytest.custom_namespace)}")
    return applitools_ultrafast_grid, applitools_execution_cloud


@pytest.fixture(scope='session')
def runner():
    """
        Create the `runner` object instance to manage Eyes visual tests. This
        fixture is ALWAYS called if a test case has the `eyes` fixture. The
        command-line flags for whether to run on grid or cloud are pulled from
        the namespace; if not explicitly specified, they default to False.

        After the test suite finishes execution, closes the batch and reports
        visual differences to the runlog. Note that it forces pytest to wait
        synchronously for all visual checkpoints to complete. Note: test results
        are not logged!

        There are 4 possible scenarios related to using Applitools:

        1. If not using a visual test (i.e., no `eyes` fixture), nothing
        happens. No Applitools logic is triggered, and this method is not
        called.

        2. Using the `eyes` fixture for a test method and including eyes.checks
        in the test method triggers Applitools logic. If there's no further
        command to use the grid or cloud, then we will run tests locally,
        which requires an instance of ClassicRunner.

        3. If using the Applitools Ultrafast Grid, create an instance of
        VisualGridRunner. For Ultrafast Grid, concurrency refers to the
        number of visual checkpoints Applitools will perform in parallel.
        Free accounts get 1.

        VisualGridRunner requires defining browser/device configurations,
        which we do with the `configuration` fixture.

        4. If using the Applitools execution cloud, a remote Chrome driver is
        instantiated in driver()

        :yield run: Appltools runner object instance
    """
    logger.info(f"\n---> namespace for applitools runner: "
                f"\n{utils.plog(pytest.custom_namespace)}")

    logger.info("\ninitializing with applitools")
    logger.info("\n-----> applitools output is logged to a different logger")
    if pytest.custom_namespace.get('applitools'):
        if pytest.custom_namespace['applitools'].get('use ultrafast grid'):
            # scenario 3
            from applitools.selenium import VisualGridRunner, RunnerOptions
            run = VisualGridRunner(RunnerOptions().test_concurrency(5))
            logger.info("\n-----> runner: visual")
            yield run

        else:
            # scenario 2
            from applitools.selenium import ClassicRunner
            run = ClassicRunner()
            logger.info("\n-----> runner: classic")
            yield run
    else:
        msg = 'runner() was called but "applitools" is missing from the namespace!'
        raise RuntimeError(msg)

    # Note: everything below in this fixture logs to runlog.txt
    # yield run
    # run.get_all_test_results()
    # logger.info(f"\nall results:\n{utils.plog(run.get_all_test_results())}")


@pytest.fixture(scope='session')
def batch_info():
    """
        Creates a new batch for tests, using a hardcoded name.
        A batch is the collection of visual checkpoints for a test suite.
        Batches are displayed in the Eyes Test Manager, so use meaningful names.

        :return batch_info: BatchInfo instance
    """
    from applitools.selenium import BatchInfo
    use_grid = None
    if pytest.custom_namespace.get('applitools'):
        if pytest.custom_namespace['applitools'].get('use ultrafast grid'):
            use_grid = pytest.custom_namespace['applitools']['use ultrafast grid']
    runner_name = "Ultrafast Grid" if use_grid else "Classic runner"
    batch_info = BatchInfo(f"Example: Selenium pytest with the {runner_name}")
    logger.info(f"\nstarted at: {batch_info.started_at}")
    logger.info(f"\nbatch info: \n{utils.plog(dir(batch_info))}")
    return batch_info


@pytest.fixture(scope='session')
def configuration(applitools_key, batch_info):
    """
        Creates a configuration for Applitools Eyes to test desktop browsers
        and mobile devices.

        Browsers are rendered in one of three ways:
        1. desktop browsers are rendered on a desktop environment:
                IE & Edge on Windows
                Safari on macOS
                other browsers on Linux
        2. Android devices are emulated with Chrome device emulation running
           on a desktop environment; specifics depend on device type.
        3. iOS devices are rendered with Safari on a mobile device simulator

        The Applitools API key is loaded into the local env
        via .bash_profile

        for device & browser options, see
        https://applitools.com/docs/topics/overview/ufg-devices.html

        browsers are configured like so:
            config.add_browser(800, 600, BrowserType.CHROME)
            config.add_browser(1600, 1200, BrowserType.FIREFOX)
            config.add_browser(1024, 768, BrowserType.SAFARI)

        mobile device browser examples:
            config.add_browser(IosDeviceInfo(IosDeviceName.iPhone_11, ScreenOrientation.PORTRAIT))
            config.add_browser(ChromeEmulationInfo(DeviceName.Nexus_10, ScreenOrientation.LANDSCAPE))

        :param applitools_key: fixture that returns str key from ENV
        :param batch_info: BatchInfo instance
    """
    # Construct the object
    config = Configuration()

    # Set the batch for the config.
    config.set_batch(batch_info)

    # Set the Applitools API key so test results are uploaded to our account.
    # If we don't explicitly set the API key with this call,
    # then the SDK will automatically read the `APPLITOOLS_API_KEY`
    # environment variable to fetch it.
    config.set_api_key(applitools_key)

    # If running tests on the Ultrafast Grid, configure browsers.
    if pytest.custom_namespace.get('applitools'):
        if pytest.custom_namespace['applitools'].get('use ultrafast grid'):
            # Add desktop browsers with different viewports for cross-browser
            config.add_browser(800, 600, BrowserType.CHROME)
            config.add_browser(1600, 1200, BrowserType.FIREFOX)

            # Add mobile browsers with different orientations
            config.add_browser(IosDeviceInfo(
                IosDeviceName.iPhone_11, ScreenOrientation.PORTRAIT))

    # Return the configuration object
    return config


@pytest.fixture(scope='function')
def eyes(runner, configuration, driver, request):
    """
    Creates the Applitools Eyes object connected to the runner `runner`
    and set its configuration. Then opens Eyes to start visual testing
    before the test, and closes Eyes at the end of the test.

    Use this as a test fixture by adding the argument `eyes` to the
    test method.

    Opening Eyes requires 4 arguments:
        1. The WebDriver object to "watch".
        2. The name of the application under test.
           All tests for the same app should share the same app name.
           Set this name wisely: Applitools features rely on a shared
           app name across tests.
        3. The name of the test case for the given application.
           Additional unique characteristics of the test may also be specified
           as part of the test name, such as localization information
           ("Home Page - EN") or different user permissions ("Login by admin").
        4. (Optional) viewport size for the local browser.
           Eyes will resize the web browser to match the requested viewport size.
           This parameter is optional but encouraged in order to produce
           consistent results.

    A test in Applitools Eyes is defined by eyes calls:
        eyes.open() starts the test
        eyes.check calls are the test steps
        eyes.close() closes the test

    more on the viewport:
        https://applitools.com/docs/topics/general-concepts/using-viewports-in-eyes.html
    """
    eyes = Eyes(runner)
    eyes.set_configuration(configuration)

    logger.info(f"\nrequest.node.name: {(request.node.name)}"
                f"\nrequest.node.module: {(request.node.module)}"
                f"\nrequest.node.nodeid: {(request.node.nodeid)}"
                f"\nrequest.node.user_properties: {(request.node.user_properties)}")

    eyes.open(
        driver=driver,
        app_name=FRAMEWORK,  # we use our framework's name; defined at file top
        test_name=request.node.name  # use collected test method name
        # viewport_size=RectangleSize(1200, 600)  # overrides selenium settings?!
    )

    logger.info(f"\ndir(eyes): {utils.plog(dir(eyes))}")
    logger.info(f"\neyes.__dict__: {utils.plog(eyes.__dict__)}")

    yield eyes
    eyes.close_async()


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


@pytest.fixture(scope='session')
def sweetshop(request):
    """
        This test fixture is a trigger for setting up authentication
        management for a generic web app.
        Note: not really, this is just an example to use for real apps
        that have actual users with real credentials in AWS.
    """
    pass
