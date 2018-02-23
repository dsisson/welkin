import logging
from welkin.apps.examples.google.base_page import PageObject
from welkin.framework.exceptions import PageIdentityException

logger = logging.getLogger(__name__)


class HomePage(PageObject):

    def __init__(self, driver):
        self.url = 'https://' + self.domain + '/'
        self.driver = driver
        logger.info('Instantiated PageObject for Google.')

    def load(self):
        """
            Load the home page for google search.

            :return:
        """
        self.driver.get(self.url)
        logger.info('Loaded Google home page.')

    def verify_self(self):
        """
            Check these specific identifiers to prove that we are on the expected page.

            :return: True if valid, else raise exception
        """
        # set expectations
        expected_title = 'Google'
        expected_domain = self.domain

        # actual results
        domain_from_url = self.driver.current_url.split('/')
        actual_title = self.driver.title
        actual_domain = domain_from_url[2]

        # validate expectations
        if actual_title == expected_title and actual_domain == expected_domain:
            logger.info('Google home page self-validated identity.')
            return True
        else:
            msg1 = 'FAIL: Google home page did NOT self-validate identity. '
            msg2 = 'Expected "%s" + "%s", got "%s" + "%s".' % \
                   (expected_title, expected_domain, actual_title, actual_domain)

            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

