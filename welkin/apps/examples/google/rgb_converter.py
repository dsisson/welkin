import logging
from welkin.apps.examples.google.results import SearchResultsPage
from welkin.framework.exceptions import PageIdentityException
from welkin.framework.exceptions import GoogleResultsCountException
from welkin.framework import utils

logger = logging.getLogger(__name__)


class ColorConverterWidget(SearchResultsPage):

    sel_color_fields = '.gws-csf-color_picker__black input'
    sel_converter_bar = 'g-inline-expansion-bar'

    def __init__(self, driver):
        self.driver = driver
        logger.info('Instantiated RGB converter widget.')

        # set up the RGB converter
        page = self.start_converter()

    def start_converter(self):
        """
            Perform the google search that triggers the color converter widget.

            :return page: page Welkin page object for the converter/search results page
        """
        page = self.search_for('RGB to Hex')
        self.validate_self()
        return page

    def validate_self(self):
        """
            Make sure that the Google RGB converter has actually been instantiated.

            :return: bool, True if validated, else raise exception
        """
        converter_bar_controls = ['Show color values', 'Show less']

        bar = self.driver.find_element_by_css_selector(self.sel_converter_bar)
        if not bar.text in converter_bar_controls:
            raise PageIdentityException('Error: not able to verify that RGB converter widget is available.')

        return True

    def change_hex_value(self, hex):
        """
            Change the hex value in the converter to the supplied value.

            :param hex: str, hexadecimal code for color (must include prepended `#`)
            :return: tuple, (new_hex_field, new_rgb_field)
        """
        # grab the input fields
        fields = self.driver.find_elements_by_css_selector(self.sel_color_fields)
        hex_field = fields[0]
        rgb_field = fields[1]

        # clear the hex field
        hex_field.clear()

        # enter the new value
        hex_field.send_keys(hex)

        # grab the updated values in the input fields
        updated_fields = self.driver.find_elements_by_css_selector(self.sel_color_fields)
        new_hex_field = updated_fields[0]
        new_rgb_field = updated_fields[1]

        return new_hex_field, new_rgb_field

