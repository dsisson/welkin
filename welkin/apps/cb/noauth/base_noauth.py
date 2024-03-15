import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.cb.base_page import BaseWrapperPageObject
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
            'About Us': ['About Us', 'About Us'],
            'Our History': ['About Us', 'Our History'],
            'How It Works': ['How It Works', 'How It Works'],
            'Start A Site': ['Start A Site', 'Start A Site'],
            'Advice & Inspiration': ['Advice & Inspiration', 'Advice & Inspiration'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.caringbridge.org'

        # we have 2 templates, which means some selectors will vary
        template_type_1 = ['cb home page', 'cb start a site page']
        template1 = True if self.name in template_type_1 else False

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1':
                    (By.CSS_SELECTOR,
                     "nav a[href$='/']" if template1 else "header a[href$='/']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR,
                                "nav a[href$='/']" if template1 else "header a[href$='/']"),
                        'po': 'cb home page',
                        'target': '/'
                    }
                }
            },
            'About Us': {
                'sel_stage1': (By.LINK_TEXT, "About Us"),
                'stage2': {
                    'About Us': {
                        'sel': (By.LINK_TEXT, "About Us"),
                        'po': 'cb about page',
                        'target': '/about-us'
                    },
                    'Our History': {
                        'sel': (By.LINK_TEXT, "History"),
                        'po': 'cb history page',
                        'target': '/about-us/history'
                    }
                }
            },
            'How It Works': {
                'sel_stage1': (By.LINK_TEXT, "How It Works"),
                'stage2': {
                    'How It Works': {
                        'sel': (By.LINK_TEXT, "How It Works"),
                        'po': 'cb how it works page',
                        'target': '/how-it-works'
                    }
                }
            },
            'Start A Site': {
                'sel_stage1': (By.LINK_TEXT, "Start A Site"),
                'stage2': {
                    'Start A Site': {
                        'sel': (By.LINK_TEXT, "Start A Site"),
                        'po': 'cb start a site page',
                        'target': '/createwebsite'
                    },
                }
            },
            'Advice & Inspiration': {
                'sel_stage1': (By.LINK_TEXT, "Advice & Inspiration"),
                'stage2': {
                    'Advice & Inspiration': {
                        'sel': (By.LINK_TEXT, "Advice & Inspiration"),
                        'po': 'cb resources page',
                        'target': '/resources'
                    },
                }
            }
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        self.save_screenshot(event)

        # get the nav bar; we have 2 templates, so we need to find the right one
        nav = self.driver.find_element(
            By.CSS_SELECTOR,
            "nav.navbar-global" if template1 else "header#masthead")

        # get the stage1 nav target element
        method1, selector1 = target_links[target1]['sel_stage1']
        stage1 = nav.find_element(method1, selector1)
        logger.info(f"\nstage1 str: '{selector1}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # get the stage2 nav target element
        method2, selector2 = target_links[target1]['stage2'][target2]['sel']

        # if target1 & target2 are the same, use stage1
        if selector1 == selector2:
            link = stage1
            logger.info(f"\nstage2 == stage1")
        else:
            link = nav.find_element(method2, selector2)
            logger.info(f"\nstage2 str: '{selector2}'")

        event = f"clicked {destination} destination link"
        name = f"{destination} destination link"

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['po']
        logger.info(f"\npo_selector: '{po_selector}'")

        # click the primary link, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, 40)})
            self.set_event(event)
            # self.save_screenshot(event)
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            nav = self.driver.find_element(
                By.CSS_SELECTOR,
                "nav.navbar-global" if template1 else "header#masthead")

            method, selector = target_links[destination]['sel_stage1']
            link = nav.find_element(method, selector)

            next_page = self._click_and_load_new_page(link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)
            self.set_event(event)
        return next_page
