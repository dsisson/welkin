import pytest
import logging

logger = logging.getLogger('ExampleTests')


class ExampleTests(object):

    def test_simple_pass(self, init):
        testdata = ['apple', 'pear', 'berry']
        assert 'berry' in testdata

    def test_simple_fail(self, init):
        testdata = ['apple', 'pear', 'berry']
        assert 'cherry' in testdata

    @pytest.mark.parametrize('data', ['apple', 'pear', 'berry', 10])
    def test_parametrized(self, init, data):
        logger.info('data = %s' % data)
        assert type(data) == str
