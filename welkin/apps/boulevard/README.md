# About this application wrapper 

Welkin is a functional end-to-end test automation framework written in Python, using pytest. 

I wrote Welkin as a
* teaching tool for custom test automation and the use of test runners
* scaffolding I can use to quickly build out a substantially custom test framework

The core welkin system supports:
* automatic download of cookie data
* automatic download of local and session storage
* automatic download of network traffic
* automatic generation of page load performance metrics 
* automatic accessibility review of each page
* automatic download of browser console messages and errors
* browser interaction event tracking (to support model updates to keep in sync with DOM changes). This is designed specifically to support DOM-manipulation frameworks like React. With Welkin, I can inspect the UI app's state and data after every/any interaction. 
* event-driven screenshots

I use Welkin as the starting point to build out a POC End-to-end test tool. I use this to probe applications to get a sense for how consistent the surfaces are (with respect to design and internal standards), how straightforward it is to automate against those surfaces, and see if I can find any bugs.

Having a quick start tool like this gets a team past the analysis-paralysis around choosing off-the-shelf test tools. It makes more sense to evaluate an effective tool and decide what specifically is needed. Personally, I believe in custom test automation because no stock tool handles the necessary modeling to effective test a complex business domain.   

I created this pull request because I wanted to get a feel for Boulevard's code, and (of course) to demonstrate my skills. This pull request includes:

* a wrapper for the boulevard marketing site. This wrapper uses an advanced page object model built on my router design pattern.
* a simple linear navigation test that moves around a limited set of pages I've modeled.
* a parametrized dynamic navigation test that accepts a list of pages, and then hits them in the specified order. 
* configuration changes to support the wrapper as a test fixture.

While the single test case doesn't specically check more than the ability to move between pages, the framework code  
* generates a lot of information on what the site is doing in the browser
* validates that every page change fully loads the targeted page, and that it is the correct page. While these tests don't "test" anything, they do check that the navigatiin in fact works.
* is designed to support a data-driven "expectation engine" for end-to-end testing: scenarios can be defined by a data model (for example, the list of page names to visit), and with the right modeling, we can predict the state and contect for every action.  

I'm happy to provide the test artefacts and logs; there's too much to put here. 
