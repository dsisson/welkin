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
* browser interaction event tracking (to support model updates to keep in sync with DOM changes)
* event-driven screenshots

I use Welkin as the starting point to build out POC End-to-end test tool. I use this to probe applications to get a sense for how consistent the surfaces are (with respect to design and internal standards), how straightforward it is to automate against those surfaces, and see if I can find any bugs.

Having a quick start tool like this gets a team past the analysis-paralysis around choosing off-the-shelf test tools. It makes more sense to evaluate an effective tool and decide what specifically is needed. Personally, I believe in custom test automation because no stock tool handles the necessary modeling to effective test a complex business domain.   

I created this pull request because I wanted to explore the odd browser rendering behavior amd very noisy console messages I saw when poking around the marketing site. This pull request includes:

* a wrapper for the Polywood marketing site. This wrapper uses an advanced page object model build on my router design pattern.
* a test file that has a simple navigation test across 7 pages.
* configuration changes to support the wrapper as a test fixture.

While the single test case doesn't specically check more than the ability to move between pages, the framework code is generating a lot of information on what the site is doing in the browser. 

I'm happy to provide the test artefacts and logs; there's too much to put here. 
