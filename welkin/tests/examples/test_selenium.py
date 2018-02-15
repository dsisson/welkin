import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.example
class ExampleSeleniumTests(object):

    @pytest.mark.selenium
    def test_google(self, init, driver):
        # driver = start_driver
        driver.get('https://google.com')

    @pytest.mark.selenium
    def test_cnn(self, init, driver):
        # driver = start_driver
        driver.get('https://cnn.com')
