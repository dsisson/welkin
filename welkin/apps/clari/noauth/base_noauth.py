import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.clari.base_page import BaseWrapperPageObject
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
            'Why Clari': ['Why Clari', 'Why Clari'],
            'Capture': ['Products', 'Capture'],
            'Groove': ['Products', 'Groove'],
            'All Use Cases': ['Solutions', 'All Use Cases'],
            'Pricing': ['Pricing', 'Pricing']
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.clari.com'

        target1, target2 = self.generate_nav_path(destination)

        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, "a.cl-header__logo-link"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, "a.cl-header__logo-link"),
                        'po': 'clari home page',
                        'target': '/'
                    }
                },
            },
            'Why Clari': {
                'sel_stage1': (By.CSS_SELECTOR, "nav a[href='/why-clari/']"),
                'stage2': {
                    'Why Clari': {
                        'sel': (By.CSS_SELECTOR, "nav a[href='/why-clari/']"),
                        'po': 'clari why page',
                        'target': '/why-clari/'
                    }
                }
            },
            'Products': {
                'sel_stage1': (By.CSS_SELECTOR, "nav a[href='/products/product-overview/']"),
                'stage2': {
                    'Capture': {
                        'sel': (By.CSS_SELECTOR, "nav div#tab-productsproducts a[href='/products/capture/']"),
                        'po': 'clari products capture page',
                        'target': '/products/capture/'
                    },
                    'Groove': {
                        'sel': (By.CSS_SELECTOR, "nav div#tab-productsproducts a[href='/products/groove/']"),
                        'po': 'clari products groove page',
                        'target': '/products/groove/'
                    }
                }
            },
            'Solutions': {
                'sel_stage1': (By.CSS_SELECTOR, "nav a[href='/solutions/use-cases/']"),
                'stage2': {
                    'All Use Cases': {
                        'sel': (By.CSS_SELECTOR, "nav div#tab-solutionsby-use-case a[href='/solutions/use-cases/']"),
                        'po': 'clari solutions usecases page',
                        'target': '/solutions/use-cases/'
                    },
                }
            },
            'Pricing': {
                'sel_stage1': (By.CSS_SELECTOR, "nav a[href='/pricing/']"),
                'stage2': {
                    'Pricing': {
                        'sel': (By.CSS_SELECTOR, "nav a[href='/pricing/']"),
                        'po': 'clari pricing page',
                        'target': '/pricing/'
                    },
                }
            }
        }

        event = f"scroll to top of {self.name}"
        scroll_to_top_of_page(self.driver)
        self.set_event(event)
        self.save_screenshot(event)

        # get the nav bar; we have 2 templates, so we need to find the right one
        nav = self.driver.find_element(By.TAG_NAME, "header")

        if target1 == target2:
            # this is a 1 stage nav element
            stage2 = target_links[target1]['stage2'][target2]
            po_selector = stage2['po']
            logger.info(f"\npo_selector (1 stage): '{po_selector}'")
            method2, selector2 = stage2['sel']

        else:
            # this is a 2 stage nav element, so we need to click the stage1 element
            # get the stage1 nav target element
            method1, selector1 = target_links[target1]['sel_stage1']
            stage1 = nav.find_element(method1, selector1)
            logger.info(f"\nstage1 str: '{selector1}'")
            logger.info(f"\nstage1 element text: '{stage1.text}'")

            # click to trigger sub menu
            msg = f"multi-stage nav action, clicked {target1}"
            self._click_element(stage1, target1, msg=msg)
            self.save_screenshot(f"click for target1")

            # re-get the nav element
            nav = self.driver.find_element(By.TAG_NAME, "header")

            # get the stage2 nav target element
            method2, selector2 = target_links[target1]['stage2'][target2]['sel']
            # get the page object identifier for the target page
            po_selector = target_links[target1]['stage2'][target2]['po']
            logger.info(f"\npo_selector: '{po_selector}'")

        stage2_link = self.driver.find_element(method2, selector2)
        logger.info(f"\nstage2 str: '{selector2}'")

        event = f"clicked {target2} destination link"
        name = f"{target2} destination link"

        # click the second stage link object, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, 40)})
            self.set_event(event)
            # self.save_screenshot(event)
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            nav = self.driver.find_element(By.TAG_NAME, "header")

            method, selector = target_links[destination]['sel_stage1']
            link = nav.find_element(method, selector)

            next_page = self._click_and_load_new_page(link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)
            self.set_event(event)
        return next_page
