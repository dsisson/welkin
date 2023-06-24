# About this application wrapper 

Welkin is a functional end-to-end test automation framework written in Python, using pytest. 

I wrote Welkin as a
* teaching tool for custom test automation and the use of xunit-style test runners
* scaffolding I can use to quickly build out a substantially custom test framework
* light-weight automation prototyping tool: automation is about experimentation, and there is no perfect tool; the critical thing is to get information fast and not over-invest or get bogged down  


The core Welkin system supports:
* Browser interaction event tracking (to support model updates to keep in sync with DOM changes). This is designed specifically to support DOM-manipulation frameworks like React. With Welkin, I can snapshot and inspect the UI app's state and data after every/any interaction. 
* Because Welkin tracks events, I can take event-driven screenshots.
* Automatic download of cookie data.
* Automatic download of local and session storage.
* Automatic download of network traffic.
* Automatic generation of page load performance metrics. 
* Automatic accessibility review of each page.
* Automatic download of browser console messages and errors.

I use Welkin as the starting point to build out a POC End-to-end test tool. I use this to probe applications to get a sense for how consistent the surfaces are (with respect to design and internal standards), how straightforward it is to automate against those surfaces, and see if I can find any bugs.

Having a quick start tool like this gets a team past the analysis-paralysis around choosing off-the-shelf test tools. It makes more sense to evaluate an effective tool and decide what specifically is needed. Personally, I believe in custom test automation because no stock tool handles the necessary modeling to effective test a complex business domain.   


# About This Pull Request

I created this pull request because I wanted to get a feel for Iodine's code, and to present my automation bona fides. 

This PR includes:
* a wrapper for the Iodine marketing site. This wrapper uses an advanced page object model built on my router design pattern.
* a simple linear navigation test that moves around a limited set of pages I've modeled.
* a parametrized dynamic navigation test that accepts a list of pages, and then hits them in the specified order. 
* configuration changes to support the wrapper as a test fixture.

While these two test cases doesn't specically check more than the ability to move between pages, the framework code  
* generates a lot of information on what the site is doing in the browser
* validates that every page change fully loads the targeted page, and that it is the correct page. While these tests don't "test" anything, they do check that the navigation in fact works.
* is designed to support a data-driven "expectation engine" for end-to-end testing: scenarios can be defined by a data model (for example, the list of page names to visit), and with the right modeling, we can predict the state and contect for every action.  

I'm happy to provide the test artefacts and logs, and to explain the design decisions. 