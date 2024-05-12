import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.arcticwolf.base_page import BaseWrapperPageObject
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
            'Solutions': ['Solutions', 'Solutions'],
            'How It Works': ['How It Works', 'How It Works'],
            'Why Arctic Wolf': ['Why Arctic Wolf', 'Why Arctic Wolf'],
            'Resources': ['Resources', 'Resources'],
            'Solution Providers': ['Partners', 'Solution Providers'],
            'Leadership': ['Company', 'Leadership'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://arcticwolf.com/'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='/']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area a[href='/']"),
                        'po': 'arcticwolf home page',
                        'target': '/'
                    }
                },
            },
            'Solutions': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='https://arcticwolf.com/solutions/']"),
                'stage2': {
                    'Solutions': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area a[href='https://arcticwolf.com/solutions/']"),
                        'po': 'arcticwolf solutions page',
                        'target': '/solutions/'
                    }
                }
            },
            'How It Works': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='/how-it-works/']"),
                'stage2': {
                    'How It Works': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area a[href='/how-it-works/']"),
                        'po': 'arcticwolf how it works page',
                        'target': '/how-it-works/'
                    },
                }
            },
            'Why Arctic Wolf': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='/why-arctic-wolf/']"),
                'stage2': {
                    'Why Arctic Wolf': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area a[href='/why-arctic-wolf/']"),
                        'po': 'arcticwolf why page',
                        'target': '/why-arctic-wolf/'
                    },
                }
            },
            'Resources': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='/resources/']"),
                'stage2': {
                    'Resources': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area a[href='/resources/']"),
                        'po': 'arcticwolf resource center page',
                        'target': '/resources'
                    },
                }
            },
            'Partners': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href='/partners/']"),
                'stage2': {
                    'Solution Providers': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area ul.mega-sub-menu a[href='/partners/solution-providers/']"),
                        'po': 'arcticwolf partners providers page',
                        'target': '/partners/solution-providers/'
                    },
                }
            },
            'Company': {
                'sel_stage1': (By.CSS_SELECTOR, "div#header-widget-area a[href$='/company/overview/']"),
                'stage2': {
                    'Leadership': {
                        'sel': (By.CSS_SELECTOR, "div#header-widget-area ul.mega-sub-menu a[href$='/company/companyleadership/']"),
                        'po': 'arcticwolf company leadership page',
                        'target': '/company/companyleadership/'
                    },
                }
            }
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        # self.save_screenshot(event)

        # get the nav bar
        # nav = self.driver.find_element(By.TAG_NAME, "nav")

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # # however, this really needs a check that *something* happened here
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        logger.info(f"\nstage2 method: '{method}'")
        logger.info(f"\nstage2 selector: '{selector}'")
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")

        # logger.info(f"\nstage2_link:{stage2_link.get_attribute('innerHTML')}")

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
                                                      actions={'unhover': (0, 5)})
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            stage2_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)

        return next_page
