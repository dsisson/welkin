import logging
import pytest

from welkin.tests import configs

logger = logging.getLogger(__name__)


@pytest.fixture()
def start_logger(request):
    """
        Configure the logging function and specify output path & filename.

        :param request: pytest request object (context of the calling test method)
        :return: True
    """
    output_path = configs.output_path(request)
    filename = '%s/log.txt' % output_path
    logging.basicConfig(filename=filename,
                        level=logging.INFO,
                        format='%(asctime)s %(name)s.py::%(funcName)s() [%(levelname)s] %(message)s')
    logger.info('Logger started.')
    return True


@pytest.fixture(scope='session')
def init(request):
    """
        Test run initialization steps.

        Use this fixture for ALL tests.

        :param request: pytest request object (context of the calling test method)
        :return: None
    """
    print('starting initializer...')
    start_logger(request)
    logger.info('Initialization fixture called.')


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
