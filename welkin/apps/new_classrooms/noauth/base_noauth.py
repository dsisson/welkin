import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.new_classrooms.base_page import BaseWrapperPageObject

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
            'Why We Exist': ['Why We Exist', 'Why We Exist'],
            'Solution Development': ['What We Do', 'Solution Development'],
            'Policy & Advocacy': ['What We Do', 'Policy & Advocacy'],
            'History': ['Who We Are', 'History'],
            'Leadership': ['Who We Are', 'Leadership'],
            'The Latest': ['The Latest', 'The Latest'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://newclassrooms.org'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href='https://newclassrooms.org']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "header a[href='https://newclassrooms.org']"),
                        'po': 'nc home page',
                        'target': '/'
                    }
                },
            },
            'Why We Exist': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href$='/why-we-exist/']"),
                'stage2': {
                    'Why We Exist': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/why-we-exist/']"),
                        'po': 'nc why we exist page' ,
                        'target': '/why-we-exist/'
                    },
                },
            },
            'What We Do': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href$='/what-we-do/']"),
                'stage2': {
                    'Solution Development': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/solution-development/']"),
                        'po': 'nc solution development page',
                        'target': '/solution-development/'
                    },
                    'Policy & Advocacy': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/policy/']"),
                        'po': 'nc policy page',
                        'target': '/policy/'
                    },
                },
            },
            'Who We Are': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href$='/who-we-are/']"),
                'stage2': {
                    'History': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/history/']"),
                        'po': 'nc history page',
                        'target': '/history/'
                    },
                    'Leadership': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/leadership/']"),
                        'po': 'nc leadership page',
                        'target': '/leadership/'
                    },
                },
            },
            'The Latest': {
                'sel_stage1': (By.CSS_SELECTOR, "header a[href$='/the-latest/']"),
                'stage2': {
                    'The Latest': {
                        'sel': (By.CSS_SELECTOR, "header a[href$='/the-latest/']"),
                        'po': 'nc latest page',
                        'target': '/the-latest/'
                    },
                },
            },
        }

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # however, this really needs a check that *something* happened here
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")
        # self._goto_and_hover(stage2_link, name=target2)
        self.save_screenshot(f"hover for target2")

        logger.info(f"\nstage2_link:{stage2_link.get_attribute('innerHTML')}")

        event = f"clicked {target2} destination link"
        name = f"destination link {target2}"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['po']
        logger.info(f"\nstage2 po_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        next_page = self._click_and_load_new_page(stage2_link,
                                                  po_selector=po_selector,
                                                  name=name,
                                                  change_url=True,
                                                  actions={'unhover': (0, 400)})
        return next_page
