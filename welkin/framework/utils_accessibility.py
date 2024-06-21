import logging
from axe_selenium_python import Axe

from welkin.framework import utils_file, utils_selenium

logger = logging.getLogger(__name__)


def generate_axe_review(pageobject, filename=None):
    """
        Perform and save accessibility checks based on the axe engine.

        The checks are run automatically for web pages handled
        by a welkin page object model. Results are written to the
        current test runs output/accessibility folder.

        NOTE: these checks may slow down the perceived page performance
        around page load in the context of test runs.

        The filename can be specified by the calling code, but the
        expectation is that this is either:
            1. an event string, because the trigger for running these
               checks could be a page object load or reload
            2. the default of the page object's name

        :param pageobject: pageobject instance for current page
        :param filename: str filename for the log file;
                         defaults to PO name
        :return: None
    """
    # instantiate axe
    axe = Axe(pageobject.driver)

    # inject axe.core into page
    axe.inject()

    event = f"Axe.core JS injected into page code for '{pageobject.name}'"
    pageobject.set_event(event)

    # run the axe accessibility checks
    axe_results = axe.run()
    # axe.run() caused the page to scroll to the bottom; scroll back to top
    utils_selenium.scroll_to_top_of_page(pageobject.driver)
    event = f"Forced page scroll to top of page '{pageobject.name}'"
    pageobject.set_event(event)

    # we don't want the full report, just the violations & some metadata,
    # so remove the unwanted stuff from the results
    unwanted_sections = ['passes', 'incomplete', 'inapplicable']
    for section in unwanted_sections:
        axe_results.pop(section)

    # set the cleaned file name
    fname = filename if filename else pageobject.name

    # write the results to a file
    utils_file.write_axe_log_to_file(axe_results, fname)

    # write as csv
    utils_file.write_axe_failures_to_csv(axe_results, fname)
