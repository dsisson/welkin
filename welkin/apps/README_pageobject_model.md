# Understanding the Welkin Page Object Model

## Application Wrappers
Welkin expects application wrappers to be written to support interactions with the applications under test; these wrappers are an internal API used by the test code to interact with and receive output from the applications. 

The most common applications under test will be (external) APIs, web apps, and services. The most effective _design pattern_ for creating a wrapper for a web app is a **page object model**.

The example wrapper for DuckDuckGo is built as a page object model, but it includes non-pageobject methods.


## Page Object Model Design Patterns
Page objects themselves have _design patterns_. 

The typical package structure for a POM wrapper is:
```
apps
    |- root_pageobject.py
    |- wrapper for app
        |- routings.py
        |- base_page.py
        |- noauth (for pages that do not require authentication)
            |- base_noauth.py
        |- auth  (for pages that DO require authentication)
            |- base_auth.py
```

### Hierarchical class structure
General methods and properties that are common across application wrappers are moved to root parent classes.

### Page Object instantiation managed through the router pattern
Interactions with the browser -- as mediated by the page object model -- that trigger navigation or page change/refresh actions render the current page object out-of-date with the current browser's state. A core design challenge is in figuring out how to manage the instantiation of new page objects or refreshing changed page objects. 

The simplest common pattern for managing instantiation is to explicitly call the page object classes from the test code. This is not a robust pattern because it makes the test code more difficult to maintain and extend. The test code should not be aware of the mechanics of transferring between page object classes; rather, the test code should more closely mimic browser interactions. 

A more robust approach is the Transporter design pattern, where you create a standalone class, separate from your page objects, whose responsibility is to take an identifier and return a page object class instance.

Welkin uses what I call the Router design pattern, which uses a Transporter-like approach but implements it _within_ the page object model class hierarchy. This pattern requires the application wrapper to have the following:
+ each page object has **a unique string identifier**, along with **checks for page load** (the page has to fully load before we try to interact with it) and **checks for page identity** (this is _this_ page and no other)
+ a **routings.py** file that provides a way to map the page object's unique identifier
+ a single method (I name this _load_pageobject_) that accepts a page object's identifier; finds, imports, and instantiates that page object; performs any available load and identity checks; performs any other desired actions around the instantiation of the new page object or transition away from the old page object; and finally returns the page object
+ browser interactions that trigger page navigation or page state changes or managed with page object class methods, and these methods call the page object instantiator method and then return the new page object


## Separating the authenticated and non-authenticated experience 
The authentication barrier for a web application is significant: once you log in or are otherwise authenticated the system can identify you and the application can access deep information about you. For example, after authenticating, web app pages might display information from your user account, information that would not be displayed if not authenticated.

Welkin differentiates between pages that do not require authentication (called **noauth**) and those that do (called **auth**). As illustrated in the wrapper tree above, the wrapper has the folders `noauth` and `auth`, with each folder getting a base page object class for its auth state.

This layout requires the **routings.py** file to have different mapping dicts for noauth and auth page objects, and also requires a mechanism for changing the auth state. The common examples for this change state are when:
+ viewing a noauth page like the login form, and successfully logging in
+ viewing an authenticated page, and successfully logging out

