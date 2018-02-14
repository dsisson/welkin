# Welkin
Welkin is a test automation framework shell written in Python and using the
pytest test runner.

Welkin is designed to support functional testing for one
or more apps in an ecosystem, as well as end-to-end testing across these apps.

Welkin provides a basic starting point for building a custom test framework; you add the
test data models, custom application wrappers, and the tests. Welkin is intended as a teaching
tool for beginning test automators; welkin is NOT a general test framdework or test tool.


## Installing welkin
Welkin is intended to be a starting point for your automation code framework, so while
there is a range of ways the code could be packaged and distributed cleanly, just fork
this project and set it up locally.

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



## Executing tests
Welkin is typically run from the command line. Pytest handles test collection
and the reporting of errors.

### Base Command
The base command (which runs all tests in the tests directory) is:

````
$ pwd
/Users/yourname/dev/welkin
$ python runner.py welkin/tests
````

However, I use a wrapper that adds some extra information to the test run.
Runner.py is a wrapper for pytest that adds a timestamp to a test run, creates an html
report for test results, allows for combined keyword and marker specifications for test
collection.

### Test Collection
Pytest supports several ways to control test collection.

1. string matches in the name path for the test methods
````
# collect and run every test with the string "example" in filename, classname, method name
$ python runner.py welkin/tests -k example
````

2. marker matches for test classes or methods
````
# collect and run every test class or test method marked with the pytest.marker "example"
$ python runner.py welkin/tests -m example
````

3. combined marker matches AND string matches
````
# collect and run every test marked with the pytest.marker "example" AND containing the string "simple"
$ python runner.py welkin/tests -m example -k simple
````

4. collecting the tests without running them
````
# collect every test marked with the pytest.marker "example" AND containing the string "simple"
$ python runner.py welkin/tests -m example -k simple --collect-only
collected 7 items
<Module 'examples/test_examples.py'>
  <Class 'ExampleTests'>
    <Instance '()'>
      <Function 'test_simple_pass'>
      <Function 'test_simple_fail'>
````

### Killing a Test Run
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
