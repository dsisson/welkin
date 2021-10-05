import pytest
import logging

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """
        Define any Command line options.
    """
    parser.addoption('--env',
                     action='store',
                     dest='environment',
                     choices=['local', 'qa', 'staging', 'prod'],
                     default='qa',
                     help='Specify environment: "local", "qa", "staging", "prod.')


@pytest.fixture(autouse=True, scope='session')
def environment(request):
    server = request.config.option.environment
    logger.info('Environment "%s" specified.' % server)
    if server == 'qa':
        return 'https://foo'
    elif server == 'staging':
        return 'https://foo'
    elif server == "prod":
        return 'https://foo'
    elif server == 'local':
        return 'http://127.0.0.1:8000'
    else:
        raise ValueError('Not a valid environment.')
