# Applitools Visual Testing Integration

Welkin can be integrated with Applitools for running visual tests, although the concepts and mechanics are a little confusing.

Welkin is primarily a functional testing framework, using pytest as the test runner. Pytest is a unit test test runner. The main roles of a test runner are to:
* collect tests
* run tests
* report on test results/outcomes
* provide some assertion helpers

Welkin drives browser automation with Selenium in the context of test methods, and applies checks in those test methods. Welkin also generates a lot of data and artefacts for deeper exploratory testing, for example extensive logs and screenshots.

Applitools' Eyes SDK allows for visual-based evaluation of web pages and screens: regular Selenium automated interactions drive browser state changes, and specific checkpoints in the test code trigger visual evaluation of the browser state.


## Create an Applitools Account
In order to integrate with Applitools, you'll need an account: [Create your free account](https://auth.applitools.com/users/register) for a free starter account.

Note: in order to use AI for evaluating your visual checkpoints, you'll have to upgrade to a paid account. In order to use the Applitools Execution Cloud, you will have request access.


## Adding Visual Checkpoints 
The first thing you need is a working functional test against a website; in Welkin this means you will use a site wrapper.

### A Functional Test
A simple browser test against a website, using a page object model wrapper, would look like the following:
```python
from welkin.apps.sweetshop.base_page import PomBootPage


def test_nav(driver, sweetshop):
    # instantiate the POM on the blank driver start page
    boot_page = PomBootPage(driver)

    # instantiate the home page object
    id = 'Home'
    home_page = boot_page.start_with('sweetshop home page')
    home_page.save_screenshot(f"{id} page loaded")

    # navigate to the Sweets page
    id = 'Sweets'
    sweets_page = home_page.select_page_from_top_menu(id)
    sweets_page.save_screenshot(f"{id} page loaded")
```

This test method takes two fixtures as arguments: 
* *sweetshop* -- the POM wrapper fixture
* *driver* -- the webdriver instance for the browser

The test instantiate the POM, then uses that to navigate to another page. In the background, Welkin logs browser information and saves screenshots. 

### Making this a Visual Test

To turn this into a visual test, we add 3 things:
* the import of Target, which is used in the Eyes test steps
* the *eyes* fixture used as an argument for the test method
* the two test steps that begin with eyes.check()

```python
from applitools.selenium import Target
from welkin.apps.sweetshop.base_page import PomBootPage


def test_nav(driver, sweetshop, eyes):
    # instantiate the POM on the blank driver start page
    boot_page = PomBootPage(driver)

    # instantiate the home page object
    id = 'Home'
    home_page = boot_page.start_with('sweetshop home page')
    home_page.save_screenshot(f"{id} page loaded")
    eyes.check(Target.window().fully().with_name(id))

    # navigate to the Sweets page
    id = 'Sweets'
    sweets_page = home_page.select_page_from_top_menu(id)
    sweets_page.save_screenshot(f"{id} page loaded")
    eyes.check(Target.window().fully().with_name(id))
```

When this test method is run, pytest runs the test functionally and gets a result, then the Eyes SDK runs the test *again* using checkpoint screenshots.

