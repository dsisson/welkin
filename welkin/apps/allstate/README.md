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

I created this pull request because I wanted to explore the errors I was easily triggering the browser as a played with the login form. This pull request includes:
* a wrapper for the AIP marketing site and teh login page for the API app. This wrapper uses an advanced page object model build on my router design pattern.
* a test file that has a simple navigation test and a parametrized unhappy login path test. With parametrization, new "test scenarios" can be added by adding data to an iterable.
* minor configuration changes to support the wrapper as a test fixture.

Below is a list of the errors I saw in the console (out of contecxt and compiled here):
```
{
    "_page": "https://app.allstateidentityprotection.com/signin",
    "console": {
        "console": [
            {
                "level": "SEVERE",
                "message": "https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js 0:91402 Error: Login required\n    at d.fromPayload (https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js:1:7608)\n    at s (https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js:1:39038)",
                "source": "console-api",
                "timestamp": 1681495512627
            },
            {
                "level": "SEVERE",
                "message": "https://tmscdn.coremetrics.com/tms/25000017/cp-v3.js?__t=20230414140512659 - Failed to load resource: the server responded with a status of 404 (Not Found)",
                "source": "network",
                "timestamp": 1681495512719
            }
        ]
    }
}

{
    "_page": "https://app.allstateidentityprotection.com/signin/forgot-password",
    "console": {
        "console": [
            {
                "level": "SEVERE",
                "message": "https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js 0:91402 \"caught an error Error: 404: Not Found\"",
                "source": "console-api",
                "timestamp": 1681495517782
            },
            {
                "level": "SEVERE",
                "message": "https://tmscdn.coremetrics.com/tms/25000017/cp-v3.js?__t=20230414140519053 - Failed to load resource: the server responded with a status of 404 (Not Found)",
                "source": "network",
                "timestamp": 1681495519126
            },
            {
                "level": "SEVERE",
                "message": "https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js 0:91402 Error: Login required\n    at d.fromPayload (https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js:1:7608)\n    at s (https://app.allstateidentityprotection.com/_next/static/chunks/pages/_app-f74d11cd73ccec5f.js:1:39038)",
                "source": "console-api",
                "timestamp": 1681495519410
            }
        ]
    }
}

{
    "_page": "https://app.allstateidentityprotection.com/signin",
    "console": {
        "console": [
            {
                "level": "SEVERE",
                "message": "javascript 2:369 Uncaught TypeError: Converting circular structure to JSON\n    --> star\u2026i'\n    --- property 'stateNode' closes the circle",
                "source": "javascript",
                "timestamp": 1681495522319
            },
            {
                "level": "SEVERE",
                "message": "javascript 2:369 Uncaught TypeError: Converting circular structure to JSON\n    --> star\u2026i'\n    --- property 'stateNode' closes the circle",
                "source": "javascript",
                "timestamp": 1681495522333
            },
            {
                "level": "SEVERE",
                "message": "javascript 2:369 Uncaught TypeError: Converting circular structure to JSON\n    --> star\u2026i'\n    --- property 'stateNode' closes the circle",
                "source": "javascript",
                "timestamp": 1681495522458
            },
            {
                "level": "SEVERE",
                "message": "javascript 2:369 Uncaught TypeError: Converting circular structure to JSON\n    --> star\u2026i'\n    --- property 'stateNode' closes the circle",
                "source": "javascript",
                "timestamp": 1681495522470
            }
        ]
    }
}
```