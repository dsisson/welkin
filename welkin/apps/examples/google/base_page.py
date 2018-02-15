
import logging
import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class PageObject(object):

    def verify_self(self, driver, path, wait_time=10):
        wait = WebDriverWait(self.driver, wait_time)
        pass

