# Welkin
Welkin is a test automation framework shell written in Python and using the
pytest test runner.

Welkin is designed to support functional testing for one
or more apps in an ecosystem, as well as end-to-end testing across these apps.

Welkin provides a basic starting point for building a custom test framework; you add the
test data models, custom application wrappers, and the tests.


## Installing welkin
These are basic instructions for setting up a welkin instance locally on a Mac; there are
ways to accomplish this on your systems.

You will need to create the following directory in your home folder: ````~/dev````

Create a virtualenv in the directory ````~/dev/venv````. Don't activate that yet.


In your ````~/.bash_profile````, add the following lines:

````
export PATH=$PATH:~/dev/venv
export PATH=$PATH:~/dev/welkin
export PYTHONPATH=$PYTHONPATH:~/dev/welkin
````

Activate the virtualenv ~/dev/venv.

Install the required modules from welkin/welkin/requirements.txt


## Executing tests
Welkin is typically run from the command line. Pytest handles test collection
and the reporting of errors. The base command (which runs all tests in the tests
directory) is:

````
$ pwd
/Users/yourname/dev/welkin/welkin
$ python runner.py tests
````

Runner.py is a wrapper for pytest that adds a timestamp to a test run, creates an html
report for test results, allows for combined keyword and marker specifications for test
collection.

To stop a test run, hit CTRL + C.


## Command Line Arguments
Optional command line arguments you can pass to welkin:
* *env* is the environment to run the tests against; the choices are 'local',
'qa', 'staging'; defaults to 'qa'. These don't work out of the box; they are placeholders
that need to be configured with the actual name and URLs.


# Troubleshooting
## No module named welkin.framework
If you see something like the following when you try to run your first tests, then you either
need to add the appropriate paths to your .bash_profile, or you need to refresh your terminal
instance to pull in the changes to .bash_profile
```
(venv) MacBook:welkin derek$ python runner.py tests/functional
Traceback (most recent call last):
  File "runner.py", line 8, in <module>
    from welkin.framework import utils
ImportError: No module named welkin.framework
```
