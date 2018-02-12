import logging
import pytest

from welkin.tests import configs

logger = logging.getLogger('Conftest')


@pytest.fixture()
def start_logger(request):
    """
        Configure the logging function and specify output path & filename.
    """
    output_path = configs.output_path(request)
    filename = '%s/log.txt' % output_path
    logging.basicConfig(filename=filename, level=logging.INFO)
    return True


@pytest.fixture(scope='session')
def init(request):
    """
        Test run initialization steps.

        Use this fixture for ALL tests.
    """
    print('starting initializer...')
    start_logger(request)


# markers, used for flagging tests for marks-based collection
smoke = pytest.mark.NAME
