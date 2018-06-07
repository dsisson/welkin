# Wrapper for genderizer.io API

[Genderize.io](https://genderize.io/) is a very cool API that allows you to determine the gender of a first name. It has a simple interface that supports only GETs and a few parameters.

An effective way to automate tests for a RESTful API is to create a wrapper in the test framework that allows you to write abstract interactions with that wrapper in your test methods.

Let's compare a simple _naive_ approach to interacting with the API from a test method to one that uses parametrization and APIabstraction via a wrapper class. Please note that this comparison actually reflects the reasonable and expected learning progression for testers learning how to write test automation: start in a straightforward way, then abstract and optimize.


## Naive Approach to Interacting with an API

Verify that the name ___Bob___ is genderized as male:

    def test_bob_is_male():
        # set up
        import requests  # listed here for convenience and clarity only

        name = 'Bob'
        ex_gender = 'male'
        base_url = 'https://api.genderize.io/'
        url = base_url + '?name=%s' % name

        # execution
        res = requests.get(url)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # test point: verify that we get back the same name that we requested
        assert res.json()['name'] == name, \
            'expected "%s", but got "%s"' % (name, res.json()['name'])

        # test point: verify the expected gender
        try:
            assert res.json()['gender'] == ex_gender, \
                'expected "%s", but got "%s"' % (ex_gender, res.json()['gender'])

        except KeyError:
            print('ERROR: no `gender` key in json response.')
            raise

This is a straightforward way to test genderize.io, but it relies on hardcoding some values, and it makes direct use of the __requests__ package to drive the API interactions. This is not a _bad_ approach to test automation, but it is also not a particularly efficient approach.

There are two ways to significantly improve this test method:
1. Generalize the test instructions to support parametrization and add a data model for the params.
2. Abstract out the API touchpoints to a wrapper class.


## Parametrizing the Test Method
Instead of having a multitude of very similar test methods, you can make the test method logic a litle bit more general, and then feed the test method a data model; the test runner's support of parametrization then dynamically creates a test method instance for each data element. This slight abstraction allows you to seperate the data being used in the test from the test instructions.

The following code will generate 3 separate test methods on collection: for Bob, for Jack, and for Sue. Assuming that the test instructions are correct and valid, adding more tests is as simple as adding a new name/gender tuple to the `names` list.

    import requests

    names = [('Bob', 'male'), ('Jack', 'male'), ('Sue', 'female')]

    @pytest.mark.parametrize('simple_name', names, ids=[n[0] for n in names])
    def test_name_for_gender(simple_name):
        # set up
        ex_name = simple_name[0]
        data = {'name': ex_name}
        ex_gender = simple_name[1]

        url = 'https://api.genderize.io/'

        # execution
        res = requests.get(url, params=data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # test point: verify that we get back the same name that we requested
        assert res.json()['name'] == ex_name, \
            'expected "%s", but got "%s"' % (ex_name, res.json()['name'])

        # test point: verify the expected gender
        try:
            assert res.json()['gender'] == ex_gender, \
                'expected "%s", but got "%s"' % (ex_gender, res.json()['gender'])

        except KeyError:
            print('ERROR: no `gender` key in json response.')
            raise


## Wrapping the API

For the wrapper, I created an ___endpoint object model___, which is like a page object mode, but for API endpoints.

With the api wrapper in place, the test case can be cleaned up to look the following:

    from welkin.apps.examples.genderize import api

    genderizer = api.GenderEndpoint()
    names = [('Bob', 'male'), ('Jack', 'male), ('Sue', 'female')]

    @pytest.mark.parametrize('simple_name', names, ids=[n[0] for n in names])
    def test_name_for_gender(simple_name):
        # set up
        ex_name = simple_name[0]
        data = {'name': ex_name}
        ex_gender = simple_name[1]

        res = genderizer.get(verbose=True, **data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # test point: verify that the json keys are correct
        assert genderizer.verify_keys_in_response(res.json().keys())

        # test point: verify that we get back the same name that we requested
        assert res.json()['name'] == ex_name, 'expected "%s", but got "%s"' \
                                           % (ex_name, res.json()['name'])

        # test point: verify that we got the expected gender assignment
        assert genderizer.got_gender(res, ex_gender)


You can see how the endpoint object is instantiated with `genderizer = api.GenderEndpoint()`, and then multiple calls on this endpoint object are made:
+ `genderizer.get(verbose=True, **data)` calls the API and gets the response
+ `genderizer.verify_keys_in_response(res.json().keys())` checks that the keys in the response are correct
+ `genderizer.got_gender(res, ex_gender)` verifies that the API returned the correct gender for the name

The project structure for the test framework containing the endpoint object model looks like this:

<pre>
welkin
    |- welkin
      |- apps
        |- examples
          |- genderize
            |- __init__.py
            |- api.py
            |- README.py  # this file
      |- data
      |- framework
        |- __init__.py
        |- exceptions.py
        |- utils.py
      |- models
      |- tests
        |- examples
          |- test_api_genderize.py
        |- configs.py
        |- conftest.py
        |- pytest.ini
    |- requirements.txt
</pre>

The api wrapper is in `welkin.apps.examples.genderize.api.py`.



