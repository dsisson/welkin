import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from welkin.apps.magnet.base_page import BaseWrapperPageObject
from welkin.framework.utils_selenium import scroll_to_top_of_page

logger = logging.getLogger(__name__)


class NoAuthBasePageObject(BaseWrapperPageObject):
    """
        Base PO class for all no-authentication pages. Any class methods
        or class properties general to all of those pages go here.
    """
    # str enum, either 'noauth' or 'auth', as appropriate
    page_auth_mode = 'noauth'

    def menu_tempate_router(self, target):
        """
            We have 3 different top nav menu structures. For `target`,
            route request to the appropriate menu template handler.

            :param target: str, nav link name for target page
            :return: method
        """
        map_destination_to_handler = {
            'Home': self.menu_2stage,
            'Magnet AXIOM Cyber': self.menu_3stage,
            'Magnet ARTIFACT IQ': self.menu_3stage,
            'OFFICER WELLNESS': self.menu_2stage,
            'STRATEGIC PARTNERS': self.menu_2stage,
            'OUR STORY': self.menu_2stage
        }
        return map_destination_to_handler[target]

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
            'Magnet AXIOM Cyber': ['PRODUCTS', 'ENTERPRISE', 'Magnet AXIOM Cyber'],
            'Magnet ARTIFACT IQ': ['PRODUCTS', 'MILITARY & INTELLIGENCE', 'Magnet ARTIFACT IQ'],
            'OFFICER WELLNESS': ['OUR COMMUNITY', 'OFFICER WELLNESS'],
            'STRATEGIC PARTNERS': ['PARTNERS', 'STRATEGIC PARTNERS'],
            'OUR STORY': ['COMPANY', 'OUR STORY']
        }
        return map_destination_to_path[target]

    def menu_2stage(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target2` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        # force to top of page
        scroll_to_top_of_page(self.driver)

        base = 'https://www.magnetforensics.com'

        target1, target2 = destination
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR,
                               ".navigation-mega-menu a[class='mega-menu-link mega-menu-logo'][href='https://www.magnetforensics.com']"),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR,
                                ".navigation-mega-menu a[class='mega-menu-link mega-menu-logo'][href='https://www.magnetforensics.com']"),
                        'po': 'magnet home page',
                        'target': '/'
                    }
                },
            },
            'OUR COMMUNITY': {
                'sel_stage1': (By.XPATH,
                               "//ul[@id='mega-menu-primary-navigation-mega-menu']//a[text()='OUR COMMUNITY']"),
                'stage2': {
                    'OFFICER WELLNESS': {
                        'sel': (By.XPATH, '//ul[@class="mega-sub-menu"]//a[text()="OFFICER WELLNESS"]'),
                        'po': 'magnet officer wellness page',
                        'target':  '/officer-wellness/',
                    },
                },
            },
            'PARTNERS': {
                'sel_stage1': (By.XPATH,
                               "//ul[@id='mega-menu-primary-navigation-mega-menu']//a[text()='PARTNERS']"),
                'stage2': {
                    'STRATEGIC PARTNERS': {
                        'sel': (By.XPATH, '//ul[@class="mega-sub-menu"]//a[text()="STRATEGIC PARTNERS"]'),
                        'po': 'magnet strategic partners page',
                        'target':  '/strategy-partners/',
                    },
                },
            },
            'COMPANY': {
                'sel_stage1': (By.XPATH,
                               "//ul[@id='mega-menu-primary-navigation-mega-menu']//a[text()='COMPANY']"),
                'stage2': {
                    'OUR STORY': {
                        'sel': (
                        By.XPATH, '//ul[@class="mega-sub-menu"]//a[text()="OUR STORY"]'),
                        'po': 'magnet our story page',
                        'target': '/our-story/',
                    },
                },
            },
        }

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1 = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # click to trigger sub menu
        msg = f"multi-stage nav action, clicked {target1}"
        self._click_element(stage1, target1, msg=msg)
        self.save_screenshot(f"click for target1")

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
        try:
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      )
            self.set_event(event)
            self.save_screenshot(f"clicked target2")
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            self.save_screenshot(f"unhover error")
            # get the link element again
            stage2_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage2_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)
        return next_page

    def menu_3stage(self, destination):
        """
            This is a 3-stage navigation interaction with the top nav.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        # force to top of page
        scroll_to_top_of_page(self.driver)

        target1, target2, target3 = destination
        # map of targets to selector and PO info
        target_links = {
            'PRODUCTS': {
                'sel_stage1': (
                    By.XPATH,
                    "//ul[@id='mega-menu-primary-navigation-mega-menu']//a[text()='PRODUCTS']"),
                'stage2': {
                    'MILITARY & INTELLIGENCE': {
                        'sel_stage2': (
                            By.XPATH,
                            '//ul[@class="mega-sub-menu"]//a[text()="MILITARY & INTELLIGENCE"][@data-has-click-event="true"]'),
                        'stage3': {
                            'Magnet ARTIFACT IQ': {
                                'sel': (By.XPATH, '//a[contains(text(), "Magnet ARTIFACT IQ")]'),
                                'po': 'magnet artifact iq page',
                                'target': '/products/magnet-artifactiq',
                            }
                        }
                    },
                    'ENTERPRISE': {
                        'sel_stage2': (By.XPATH,
                                       '//ul[@class="mega-sub-menu"]//a[text()="ENTERPRISE"][@data-has-click-event="true"]'),
                        'stage3': {
                            'Magnet AXIOM Cyber': {
                                'sel': (By.XPATH,
                                        '//a[contains(text(), "Magnet AXIOM Cyber")]'),
                                'po': 'magnet axiom cyber page',
                                'target':  '/products/magnet-axiom-cyber',
                            }
                        }
                    },
                },
            },
        }

        # get the stage1 nav target element
        method, selector = target_links[target1]['sel_stage1']
        stage1_target = self.driver.find_element(method, selector)
        logger.info(f"\nstage1 str: '{selector}'")
        logger.info(f"\nstage1 element text: '{stage1_target.text}'")

        # # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # # however, this really needs a check that *something* happened here
        # force to top of page
        scroll_to_top_of_page(self.driver)
        self._goto_and_hover(stage1_target, name=target1)
        event = f"hovered {target1} stage1 link"
        self.set_event(event)
        self.save_screenshot(f"hover for target1")

        # get the second menu
        menu2 = self.driver.find_element(By.XPATH, f"{selector}/following-sibling::ul/li")

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel_stage2']
        stage2_target = menu2.find_element(method, selector)
        logger.info(f"\nstage2_target selector str: '{selector}'")

        # force to top of page
        scroll_to_top_of_page(self.driver)

        # click stage 2 target on the first sub menu to display stage 3 targets
        # click to trigger sub menu
        msg = f"multi-stage nav action, clicked {target2}"
        self._click_element(stage2_target, target2, msg=msg)
        self.save_screenshot(f"before sleep")
        time.sleep(2)
        event = f"clicked {target2} stage2 link"
        self.set_event(event)
        self.save_screenshot(f"click target2")
        # time.sleep(2)

        # get the third menu
        menu3 = self.driver.find_element(By.XPATH, f"{selector}/following-sibling::ul")
        logger.info(f"\nmenu3 selector str: '{selector}/following-sibling::ul'")

        # get the stage 3 target
        method, selector = target_links[target1]['stage2'][target2]['stage3'][target3]['sel']
        stage3_link = menu3.find_element(method, selector)
        logger.info(f"\nstage3_link selector str: '{selector}'")

        # force to top of page
        for i, loop in enumerate('foo'):
            # there's a problem interacting with site
            msg = f"scroll-up {i}"
            scroll_to_top_of_page(self.driver)
            self.set_event(event_name=msg)
            self.save_screenshot(msg)

        # mouse over target 3
        self._goto_and_hover(stage3_link, name=target3)
        self.save_screenshot(f"mouseover target3")

        # get the page object identifier for the target page
        po_selector = target_links[target1]['stage2'][target2]['stage3'][target3]['po']

        event = f"clicked {target3} destination link"
        name = f"destination link {target3}"

        self.save_screenshot(f"attempt target3")
        # click the primary link, which will load the new page object
        try:
            next_page = self._click_and_load_new_page(stage3_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True,
                                                      actions={'unhover': (0, -100)})
            self.set_event(event)
            self.save_screenshot(f"clicked target3")
        except MoveTargetOutOfBoundsException:
            logger.error(f"\nunhover problem; retrying without hover")
            # get the link element again
            stage3_link = self.driver.find_element(method, selector)
            next_page = self._click_and_load_new_page(stage3_link,
                                                      po_selector=po_selector,
                                                      name=name,
                                                      change_url=True)
        return next_page

    def select_page_from_top_menu(self, target):
        """
            Wrapper to get the appropriate path and handler method
            for the requested destination page.

            :param target: str, link text for target page
            :return:
        """
        # get the path through stages
        path = self.generate_nav_path(target)

        # get the appropriate handler
        handler = self.menu_tempate_router(target)

        # run the handler
        next_page = handler(path)
        return next_page

    def handle_cookie_modal(self):
        """
            Simple and limited way to get rid of the cookies modal;
            always choose "Deny".

        :return: None
        """
        sel_modal = (By.CSS_SELECTOR, 'div.CybotCookiebotDialogContentWrapper')
        sel_decline = (By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyButtonDecline')

        # get the modal object
        modal = self.driver.find_element(sel_modal[0], sel_modal[1])
        self.save_screenshot('modal displayed')

        msg = 'clicked to close the cookies modal'
        # get the "Deny" button
        button_decline = modal.find_element(sel_decline[0], sel_decline[1])
        self._click_element(button_decline, 'odal closer', msg=msg)

        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until_not(EC.visibility_of_element_located(sel_modal))
        except TimeoutException:
            logger.error(f"\nTimed out waiting for the absence of modal")
            raise

        self.save_screenshot('modal closed')

    def handle_message(self):
        """
            Simple and limited way to get rid of the adbar.

        :return: None
        """
        sel_close = (By.XPATH, '//div[@class="sumome-react-svg-image-container"]/following-sibling::div')

        # get the close "X" element
        close_button = self.driver.find_element(sel_close[0], sel_close[1])
        self.save_screenshot('adbar displayed')

        # click the closer button
        msg = 'clicked to close adbar'
        self._click_element(close_button, 'adbar closer', msg=msg)

        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until_not(EC.visibility_of_element_located(sel_close))
        except TimeoutException:
            logger.error(f"\nTimed out waiting for the absence of adbar")
            raise
        self.save_screenshot('adbar closed')

        msg = 'unhover shift to x=-50, y=-20'
        self._unhover(x=-50, y=-20)
        self.set_event(event_name=msg)
