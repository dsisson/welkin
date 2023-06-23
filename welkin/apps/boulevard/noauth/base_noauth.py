import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from welkin.apps.boulevard.base_page import BaseWrapperPageObject

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
            'Salon': ['Industries', 'Salon'],
            'For Owners': ['Industries', 'For Owners'],
            'Features': ['Features', 'Features'],
            'Self-Booking': ['Features', 'Self-Booking'],
            'Contact Center': ['Features', 'Contact Center'],
            'Blog': ['Resources', 'Blog'],
            'Success Stories': ['Resources', 'Success Stories'],
            'Our Story': ['Company', 'Our Story'],
            'Customer Love': ['Company', 'Customer Love'],
            'Pricing': ['Pricing', 'Pricing']
        }
        return map_destination_to_path[target]

    def select_page_from_top_menu(self, destination):
        """
            This is a multi-stage navigation interaction with the top nav.
            Click `target1` to navigate to the targeted page.

            :param destination: str, identifier text for desired destination
            :return next_page: page object
        """
        base = 'https://www.joinblvd.com/'

        target1, target2 = self.generate_nav_path(destination)
        # map of targets to selector and PO info
        target_links = {
            'Home': {
                'sel_stage1': f"//nav//a[@aria-label='Home']",
                'stage2': {
                    'Home': {
                        'sel': f"//nav//a[@aria-label='Home']",
                        'po': 'boulevard home page',
                        'target': '/'
                    }
                },
            },
            'Industries': {
                'sel_stage1': f"//nav//span[text()='Industries']",
                'stage2': {
                    'Salon': {
                        'sel': f"//nav//a[text()='Salon']",
                        'po': 'boulevard salon page',
                        'target': '/salon_software'
                    },
                    'For Owners': {
                        'sel': f"//nav//a[text()='For Owners']",
                        'po': 'boulevard owners page',
                        'target': '/owners'
                    },
                },
            },
            'Features': {
                'sel_stage1': f"//nav//span[text()='Features']",
                'stage2': {
                    'Features': {
                        'sel': f"//nav//a[text()='Features']",
                        'po': 'boulevard features page',
                        'target': '/features'
                    },
                    'Self-Booking': {
                        'sel': f"//nav//a[text()='Self-Booking']",
                        'po': 'boulevard self-booking page',
                        'target': '/features/self-booking'
                    },
                    'Contact Center': {
                        'sel': f"//nav//a[text()='Contact Center']",
                        'po': 'boulevard contact center page',
                        'target': '/features/contact-center'
                    },
                },
            },
            'Resources': {
                'sel_stage1': f"//nav//span[text()='Resources']",
                'stage2': {
                    'Blog': {
                        'sel': f"//nav//a[text()='Blog']",
                        'po': 'boulevard blog page',
                        'target': '/blog'
                    },
                    'Success Stories': {
                        'sel': f"//nav//a[text()='Success Stories']",
                        'po': 'boulevard success stories page',
                        'target': '/blog?resourceId=customer-success-story'
                    },
                },
            },
            'Company': {
                'sel_stage1': f"//nav//span[text()='Company']",
                'stage2': {
                    'Our Story': {
                        'sel': f"//nav//a[text()='Our Story']",
                        'po': 'boulevard our story page',
                        'target': '/about'
                    },
                    'Customer Love': {
                        'sel': f"//nav//a[text()='Customer Love']",
                        'po': 'boulevard customer love page',
                        'target': '/love'
                    },
                },
            },
            'Pricing': {
                'sel_stage1': f"//nav//span[text()='Pricing']",
                'stage2': {
                    'Pricing': {
                        'sel': f"//nav//a/span[text()='Pricing']",
                        'po': 'boulevard pricing page',
                        'target': '/pricing'
                    }
                },
            },
        }

        # get the stage1 nav target element
        stage1 = self.driver.find_element(By.XPATH, target_links[target1]['sel_stage1'])
        logger.info(f"\nstage1 str: '{target_links[target1]['sel_stage1']}'")
        logger.info(f"\nstage1 element text: '{stage1.text}'")

        # mouseover to trigger the sub menu (no worries if there is no sub-menu)
        # however, this really needs a check that *something* happened here
        self._goto_and_hover(stage1, name=destination)
        self.save_screenshot(f"hover for target1")

        # get the stage2 nav target element
        stage2_link = self.driver.find_element(By.XPATH, target_links[target1]['stage2'][target2]['sel'])
        logger.info(f"\nstage2 str: '{target_links[target1]['stage2'][target2]['sel']}'")
        # self._goto_and_hover(stage2_link, name=target2)
        # self.save_screenshot(f"hover for target2")

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
                                                  actions={'unhover': True})
        return next_page
