import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.wordly.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def generate_nav_path(self, target):
        """
            Convert the desired `target` str into a list of two str nav targets,
            where the first is an activator for a dynamic sub-menu, and the
            second is the actual desired page.

            :param target:
            :return: list of stage1 and stage 2 nav targets
        """
        map_destination_to_path = {
            'Home': ['Home', 'Home'],
            'Ai Captioning': ['Solutions', 'Ai Captioning'],
            'Meeting Translation': ['Use Cases', 'Meeting Translation'],
            'All Use Cases': ['Use Cases', 'All Use Cases'],
            'About Us': ['Company', 'About Us'],
            'Why Wordly': ['Company', 'Why Wordly'],
            'How Wordly Works': ['Resources', 'How Wordly Works'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.wordly.ai'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, ".nav-container a[aria-label='home']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[aria-label='home']"),
                        'po': 'wordly home page',
                        'target': '/'
                    }
                },
            },
            'Solutions': {
                'sel_stage1': (By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' nav-container ')]"
                                         "//div[text()='Solutions']"),
                'stage2': {
                    'Ai Captioning': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/ai-captioning']"),
                        'po': 'wordly ai captioning page',
                        'target': '/ai-captioning'
                    },
                }
            },
            'Use Cases': {
                'sel_stage1': (By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' nav-container ')]"
                                         "//div[text()='Use Cases']"),
                'stage2': {
                    'Meeting Translation': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/meeting-interpretation']"),
                        'po': 'wordly meeting translation page',
                        'target': '/meeting-interpretation'
                    },
                    'All Use Cases': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/translation-services']"),
                        'po': 'wordly all use cases page',
                        'target': '/translation-services'
                    }
                }
            },
            'Company': {
                'sel_stage1': (By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' nav-container ')]"
                                         "//div[text()='Company']"),
                'stage2': {
                    'About Us': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/real-time-translation']"),
                        'po': 'wordly about us page',
                        'target': '/real-time-translation'
                    },
                    'Why Wordly': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/audio-translation']"),
                        'po': 'wordly why page',
                        'target': '/audio-translation'
                    }
                }
            },
            'Resources': {
                'sel_stage1': (By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' nav-container ')]"
                                         "//div[text()='Resources']"),
                'stage2': {
                    'How Wordly Works': {
                        'sel': (By.CSS_SELECTOR, ".nav-container a[href='/translation-software']"),
                        'po': 'wordly how wordly works page',
                        'target': '/translation-software'
                    },
                }
            },
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        # self.save_screenshot(event)

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # click to trigger the submenu
        self._click_element(stage1, name='dropdown trigger')

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        logger.info(f"\nstage2 method: '{method}'")
        logger.info(f"\nstage2 selector: '{selector}'")
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")

        event = f"clicked {target2} destination link"
        name = f"destination link {target2}"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['po']
        logger.info(f"\nstage2 po_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, 400)})
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            stage2_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)

        return next_page
