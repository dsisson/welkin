import pytest
import logging

logger = logging.getLogger('Configs')


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

    parser.addoption('--output_target',
                     action='store',
                     dest='output_path',
                     help='Specify an output path for test-generated artefacts, e.g. logs.')

    parser.addoption('--timestamp',
                     action='store',
                     dest='timestamp',
                     help='Specify the timestamp for this test run.')


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


@pytest.fixture(autouse=True, scope='session')
def output_path(request):
    output_path = request.config.option.output_path
    logger.info('output path is "%s".' % output_path)
    return output_path


@pytest.fixture(autouse=True, scope='session')
def timestamp(request):
    timestamp = request.config.option.timestamp
    logger.info('timestamp is "%s".' % timestamp)
    return timestamp
