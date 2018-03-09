import logging
import pytest
import time
import sys
from pathlib import Path

from welkin.framework import utils

logger = logging.getLogger(__name__)


def pytest_configure(config):
    """
        Set up the output folder, logfile, and html report file; this has to be done right after
        the command line options are parsed, because we need to rewrite the pytest-html path.

        This requires that pytest.in includes the following line so that there is an htmlpath attribute
        to modify:
            addopts = --html=output/report.html

        :param config: pytest Config object
        :return: None
    """
    # set the timestamp for the start of this test run; this is used globally for this run
    timestamp = time.strftime('%y%m%d-%H%M%S')
    config.timestamp = timestamp  # allow for global access

    # create the output folder for this test run
    output_path = utils.generate_output_path(timestamp)
    folder = utils.create_output_folder(output_path)

    # start logging
    filename = '%s/log.txt' % output_path
    logging.basicConfig(filename=filename,
                        level=logging.INFO,
                        format='%(asctime)s %(name)s::%(funcName)s() [%(levelname)s] %(message)s')

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


@pytest.yield_fixture(scope="function")
def driver(request):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # default wait for 10 seconds
    logger.info('Starting driver.')
    yield driver
    driver.quit()
    logger.info('Quiting driver.')


# markers, used for flagging tests for marks-based collection
example = pytest.mark.NAME  # for tests used as examples for this framework
smoke = pytest.mark.NAME
selenium = pytest.mark.NAME  # for tests requiring selenium
api = pytest.mark.NAME
