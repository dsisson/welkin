# welkin


## Table of Contents
+ [What is Welkin?](#what-is-welkin)
    + [What Welkin is Not](#what-welkin-is-not)
    + [Wait, what?](#wait-what)
+ [Installing Welkin](#installing-welkin)
+ [Running Welkin](#running-welkin)
    + [Base Command](#base-command)
    + [Controlling The Collected Tests](#controlling-the-collected-tests)
    + [Collecting Tests Without Running Them](#collecting-tests-without-running-them)
    + [Killing a Test Run](#killing-a-test-run)
    + [Command Line Arguments](#command-line-arguments)
    + [Logging](#logging)
+ [Linting with Flake8](#linting-with-flake8)
+ [Automation Examples](#automation-examples)
    + [Single-Endpoint API](#single-endpoint-api)
+ [See Also](#see-also)


## What is Welkin?
Welkin is a test automation framework shell written in Python and using the pytest test runner.

Welkin is designed to support functional testing for one or more apps in an ecosystem, as well as end-to-end testing across these apps.

Welkin provides a basic starting point for building a custom test framework; you add the test data models, custom application wrappers, and the tests. Welkin is intended as a teaching tool for beginning test automators; welkin is NOT a general test framework or test tool.

### What Welkin is Not
Welkin is not a test framework, because
+ it doesn't have a body of tests beyond simple demonstration examples;
+ it doesn't have any application models or wrappers.

Welkin is a scaffolding on which a custom test automation framework can be built.

And Welkin is not a turn-key tool; you will need to modify Welkin to make it useful for your test needs.

### Wait, what?
Ok, here's the context behind welkin:
+ A robust and useful test automation framework requires a test runner
to collect, execute, and report on tests. _Welkin is built around the pytest test runner, and relies on pytest for test collection, test execution, and the reporting of test results._
+ A test framework needs to manage how and where the test results are reported,
along with managing the logging of test activity. _Welkin creates date and timestamped logs and html test results into a testrun-specific output folder._
+ A test framework needs a body of tests in a place where the test runner can find them.
_Welkin is just a scaffolding, so it provides some example tests to show
how this all works together._
+ A test framework probably should provide support for abstracting out some test logic so that tests can be written at higher level.
+ A test framework should provide a mechanism for abstracting out test data from the tests.
+ A test framework should provide tools and utilities to support test activities,
and to abstract out repeated supporting actions from the tests.

A test framework should be customized to the specific business domain you are working in, and to the applications under test.


## Installing Welkin
Welkin is intended to be a starting point for your automation code framework, so while there is a range of ways the code could be packaged and distributed cleanly, just fork this project and set it up locally.

What I do is:
+ think up a cool name for the test automation framework I'm __going__ to build
+ clone the code to a local repo
+ set up a virtualenv
+ run requirements.txt
+ add mappings to the local welkin project in my bash profile
+ create a new repo on github for the new framework (Welkin has done it's job)


You will need to create the following directory in your home folder: ````~/dev````

Create a virtualenv in the directory ````~/dev/venv````. Don't activate that yet.


On a Mac, you'll probably have to add mappings in your bash profile to the project:

````
export PATH=$PATH:~/dev/venv
export PATH=$PATH:~/dev/welkin
export PYTHONPATH=$PYTHONPATH:~/dev/welkin
````

Activate the virtualenv ~/dev/venv.

### And Then There's ChromeDriver
You will need a recent version of the Chrome browser on your local system, as well as the matching Chromedriver executable (see https://sites.google.com/chromium.org/driver/?pli=1) installed in your virtualenv, specifically in:

```~/dev/venv/bin```

I would also suggest you keep a separate collection of old versioned drivers like this (the exe file doesn't have any versioning in the filename):

```
dev
  |- drivers
    |- chrome
      |- 95.0.4638.17
        |- chromedriver.exe
```


## Running Welkin
Welkin is typically run from the command line. Pytest handles test collection and the reporting of errors.

### Base Command
The base command to collect and run tests with pytest is the following:
````
$ cd <path_to_welkin>
# you should be in the top-level welkin folder
$ pytest welkin/tests
````


### Controlling The Collected Tests
Pytest supports several ways to control test collection.

1. string matches in the name path for the test methods
````
# collect and run every test with the string "example" in filename, classname, method name
$ pytest welkin/tests -k example
````

2. marker matches for test classes or methods
````
# collect and run every test class or test method marked with the pytest.marker "example"
$ pytest welkin/tests -m example
````

3. combined marker matches AND string matches
````
# collect and run every test marked with the pytest.marker "example" AND containing the string "simple"
$ pytest welkin/tests -m example -k simple
````


### Collecting Tests Without Running Them
Sometimes you'll need to collect but not run tests:
````
# collect every test marked with the pytest.marker "example" AND containing the string "simple"
$ pytest welkin/tests -m example -k simple --collect-only
collected 7 items
<Module 'examples/test_examples.py'>
  <Class 'ExampleTests'>
    <Instance '()'>
      <Function 'test_simple_pass'>
      <Function 'test_simple_fail'>
````


### Killing a Test Run
To stop a test run, hit CTRL + C.


### Command Line Arguments
Optional command line arguments you can pass to welkin:
* *env* is the environment to run the tests against; the choices are 'local',
'qa', 'staging'; defaults to 'qa'. These don't work out of the box; they are placeholders
that need to be configured with the actual name and URLs.


### Logging
Welkin is intended to be verbose in its logging; however, that's up to you to implement as you build out your own framework.

By default, Welkin creates an output folder at welkin/output, and then for each test run Welkin creates a folder in _output_ named with the testrun's timestamp; this folder gets the HTML test results page, plus the text log of test run activity. This output is not automatically cleaned up. You'll have to define a workflow for this, if you want.


## Linting with Flake8
From the [**Flake8** description](https://flake8.pycqa.org/en/latest/manpage.html):

"Flake8 is a command-line utility for enforcing style consistency across Python projects. By default it includes lint checks provided by the PyFlakes project, PEP-0008 inspired style checks provided by the PyCodeStyle project, and McCabe complexity checking provided by the McCabe project. It will also run third-party extensions if they are found and installed."

Running flake8 against the welkin codebase:
```
# from the project directory
$ flake8 > output/flake8.txt
```

Specific configuration instructions can be set in ```setup.cfg```.



## Automation Examples
Some examples of solving particular automation challenges.

### Single-Endpoint API
see [Wrapper for genderizer API](welkin/apps/examples/genderize/README.md)

# See Also
* [Understanding Welkin's page object model](welkin/apps/README_pageobject_model.md)
* [Setting up AWS integration](welkin/integrations/aws/README_aws.md)
* [Applitools Visual Testing Integration](welkin/integrations/applitools/README_applitools.md)
