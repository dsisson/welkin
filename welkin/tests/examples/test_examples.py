import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.example
class ExampleTests(object):

    def test_simple_pass(self, init):
        """
            A simple test method that looks for the presence of a string in a list of strings.

            :param init: pytest fixture that turns on logging
            :return: None
        """
        testdata = ['apple', 'pear', 'berry']
        expected_element = 'berry'
        logger.info('Looking for "%s".' % expected_element)
        assert expected_element in testdata, 'FAIL: "%s" not in "%s".' % (expected_element, testdata)

    def test_simple_fail(self, init):
        """
            A simple test method that looks for the presence of a string in a list of strings, but fails.

            :param init: pytest fixture that turns on logging
            :return: None
        """
        testdata = ['apple', 'pear', 'berry']
        expected_element = 'cherry'
        logger.info('Looking for "%s".' % expected_element)
        assert expected_element in testdata, 'FAIL: "%s" not in "%s".' % (expected_element, testdata)

    @pytest.mark.parametrize('fruit', [
                                      'apple',
                                      'pear',
                                      'berry',
                                      pytest.mark.xfail('kumquat')])
    def test_parametrized(self, init, fruit):
        """
            A parametrized test method that looks for the presence of a string in a list of strings.
            A test instance is created for each parameter in the supplied list; one of these instances
            will fail.

            :param init: pytest fixture that turns on logging
            :fruit: str, item in the parametrized list to test for
            :return: None
        """
        testdata = ['apple', 'pear', 'berry']
        expected_element = fruit
        logger.info('Looking for "%s".' % expected_element)
        assert expected_element in testdata, 'FAIL: "%s" not in "%s".' % (expected_element, testdata)

    def test_zero_division(self, init):
        """
            Looking for the correct exception to be raised when dividing by zero.

            :param init: pytest fixture that turns on logging
            :return: None
        """
        with pytest.raises(ZeroDivisionError) as excinfo:
            1 / 0  # divide by zero
        assert 'division by zero' in str(excinfo.value)
        logger.info('excinfo.value = "%s".' % str(excinfo.value))
