import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.iodine.base_page import BaseWrapperPageObject

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
            'why iodine': ['why iodine', 'why iodine'],
            'AwareCDI': ['solutions', 'AwareCDI'],
            'Interact': ['solutions', 'Interact'],
            'CognitiveML': ['solutions', 'CognitiveML'],
            'ChartWiseCDI': ['solutions', 'ChartWiseCDI'],
            'news & insights': ['news & insights', 'news & insights'],
            'About': ['company', 'About'],
            'Partnerships': ['company', 'Partnerships'],
            'Contact': ['company', 'Contact'],
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://iodinesoftware.com/'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': (By.CSS_SELECTOR, 'a[href="/"]'),
                'stage2': {
                    'Home': {
                        'sel': (By.CSS_SELECTOR, 'a[href="/"]'),
                        'po': 'iodine home page',
                        'target': '/'
                    }
                },
            },
            'why iodine': {
                'sel_stage1': (By.LINK_TEXT, 'why iodine'),
                'stage2': {
                    'why iodine': {
                        'sel': (By.LINK_TEXT, 'why iodine'),
                        'po': 'iodine why page',
                        'target': '/why-iodine/'
                    },
                },
            },
            'solutions': {
                'sel_stage1': (By.LINK_TEXT, 'solutions'),
                'stage2': {
                    'AwareCDI': {
                        'sel': (By.XPATH, '//h4[text()="AwareCDI"]'),
                        'po': 'iodine aware cdi page',
                        'target': '/aware-cdi/'
                    },
                    'Interact': {
                        'sel': (By.XPATH, '//h4[text()="Interact"]'),
                        'po': 'iodine interact page',
                        'target': '/interact/'
                    },
                    'CognitiveML': {
                        'sel': (By.XPATH, '//h4[text()="CognitiveML"]'),
                        'po': 'iodine cognitiveml page',
                        'target': '/cognitive-ml/'
                    },
                    'ChartWiseCDI': {
                        'sel': (By.XPATH, '//h4[text()="ChartWiseCDI"]'),
                        'po': 'iodine chartwise page',
                        'target': '/chartwise/'
                    },
                },
            },
            'news & insights': {
                'sel_stage1': (By.LINK_TEXT, 'news & insights'),
                'stage2': {
                    'news & insights': {
                        'sel': (By.LINK_TEXT, 'news & insights'),
                        'po': 'iodine news insights page',
                        'target': '/news-and-insights/'
                    },
                },
            },
            'company': {
                'sel_stage1': (By.LINK_TEXT, 'company'),
                'stage2': {
                    # 'About': {
                    #     'sel': (By.XPATH, '//h4[text()="About"]/../../..'),
                    #     'po': 'iodine about page',
                    #     'target': '/about-us/'
                    # },
                    'About': {
                        'sel': (By.CSS_SELECTOR, 'a[href$="/about-us/"]'),
                        'po': 'iodine about page',
                        'target': '/about-us/'
                    },
                    'Partnerships': {
                        'sel': (By.CSS_SELECTOR, 'a[href$="/partnerships/"]'),
                        'po': 'iodine partnerships page',
                        'target': '/partnerships/'
                    },
                    'Contact': {
                        'sel': (By.CSS_SELECTOR, 'a[href$="/contact-us/"]'),
                        'po': 'iodine contact us page',
                        'target':'/contact-us/'
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
        # self.save_screenshot(f"hover for target1")

        # get the stage2 nav target element
        method, selector = target_links[target1]['stage2'][target2]['sel']
        stage2_link = self.driver.find_element(method, selector)
        logger.info(f"\nstage2 str: '{selector}'")
        # self._goto_and_hover(stage2_link, name=target2)
        # self.save_screenshot(f"hover for target2")

        # force browser to open link in the current tab
        logger.info(f"\ncurrent target:{self.driver.execute_script('arguments[0].target;', stage2_link)}")
        self.driver.execute_script("arguments[0].target='_self';", stage2_link)

        logger.info(f"\nstage2_link:{stage2_link.get_attribute('innerHTML')}")

        # change the rel value from 'noopener' to 'opener'
        self.driver.execute_script("arguments[0].rel='opener';", stage2_link)

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
                                                  actions={'unhover': (-100, 200)})
        return next_page
