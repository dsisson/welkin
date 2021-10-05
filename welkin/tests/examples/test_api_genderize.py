import pytest
import logging

from welkin.framework import utils
from welkin.apps.examples.genderize import api
from welkin.apps.examples.genderize.genderize_data import good_names_single
from welkin.apps.examples.genderize.genderize_data import good_names_multiple
from welkin.apps.examples.genderize.genderize_data import bad_names_single
from welkin.apps.examples.genderize.genderize_data import bad_names_multiple
from welkin.apps.examples.genderize.genderize_data import too_many_names

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.api
class ExampleGenderizerTests(object):

    gender_endpoint = api.GenderEndpoint()

    @pytest.mark.parametrize('good_name',
                             [n for n in good_names_single],
                             ids=[n[0] for n in good_names_single])
    def test_get_single_name(self, genderizer, good_name):
        """
            For the supplied name and expected gender, verify that the API
            response contains the name and expected gender.

            :param good_name: tuple, str name and str gender
            :return: None
        """
        api = self.gender_endpoint
        name = good_name[0]
        expected_name = good_name[0]
        ex_gender = good_name[1]

        res = api.get_gender(name, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that we get back the same name that we requested
        assert res.json()['name'] == expected_name, \
            'expected "%s", but got "%s"' \
            % (expected_name, res.json()['name'])

        # test point: verify that we got the expected gender assignment
        assert api.got_gender(res, ex_gender)

        # test point: verify that the json keys are correct
        assert api.verify_keys_in_response(res.json().keys())

        # test point: verify that the json schema is correct
        # using the new schema validator approach
        assert api.validate_schema(res.json(), verbose=True)

    @pytest.mark.parametrize('multiple_good_names', [n for n in good_names_multiple],
                             ids=['+'.join(l[0]) for l in good_names_multiple])
    def test_get_multiple_good_names(self, genderizer, multiple_good_names):
        """
            For the supplied list of names and expected genders, verify that
            the API response contains the names and expected genders.

            :param multiple_good_names: tuple, list of str names and list of str genders
            :return: None
        """
        api = self.gender_endpoint
        names = list(multiple_good_names[0])

        res = api.get_gender(names, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # convert the param from list of names + list of genders
        # to list of name + gender pairs
        expected = list(zip(multiple_good_names[0], multiple_good_names[1]))
        logger.info('expected: %s' % expected)

        # convert the returned json into a list of name + gender pairs
        actual = [(n['name'], n['gender']) for n in res.json()]
        logger.info('actual: %s' % actual)

        # test point: verify that the json keys are correct for the first item
        assert api.verify_keys_in_response(res.json()[0].keys())

        # test point: verify that the json schema is correct
        # using the new schema validator approach
        assert api.validate_schema(res.json()[0], verbose=True)

        # test point: verify a results item for each name passed to the API
        assert len(expected) == len(actual), \
            'FAIL: got %s results but expected %s.' \
            % (len(actual), len(expected))

        # loop over the results and validate each name/gender pair
        for i, item in enumerate(actual):

            # test point: verify that we get back the same name that we requested
            assert item[0] == expected[i][0], \
                'expected "%s", but got "%s"' % (expected[i][0], item[0])

            # test point: verify the expected gender for the name
            assert item[1] == expected[i][1], \
                'expected "%s", but got "%s"' % (expected[i][1], item[1])

    @pytest.mark.parametrize('bad_name', [n for n in bad_names_single])
    def test_gender_not_resolved(self, genderizer, bad_name):
        """
            For the supplied problematic name, verify that the API response
            contains the name and null gender.

            :param bad_name: str name
            :return: None
        """
        api = self.gender_endpoint
        name = bad_name
        ex_gender = None

        res = api.get_gender(name, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that we get back the same name that we requested
        assert res.json()['name'] == bad_name, \
            'expected "%s", but got "%s"' % (bad_name, res.json()['name'])

        # verify that we got gender assignment of None
        assert self.gender_endpoint.got_gender(res, ex_gender)

    @pytest.mark.parametrize('multiple_bad_names', [n for n in bad_names_multiple],
                             ids=['+'.join(l[0]) for l in bad_names_multiple])
    def test_get_multiple_bad_names(self, genderizer, multiple_bad_names):
        """
            For the supplied list of names and expected genders, verify that
            the API response contains the names and expected genders.

            :param multiple_bad_names: tuple, list of str names and list of str genders
            :return: None
        """
        api = self.gender_endpoint
        name = list(multiple_bad_names[0])

        res = api.get_gender(name, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # convert the param from list of names + list of genders
        # to list of name + gender pairs
        expected = list(zip(multiple_bad_names[0], multiple_bad_names[1]))
        logger.info('expected: %s' % expected)

        # convert the returned json into a list of name + gender pairs
        actual = [(n['name'], n['gender']) for n in res.json()]
        logger.info('actual: %s' % actual)

        # test point: verify that the json keys are correct for the first item
        assert api.verify_keys_in_response(res.json()[0].keys())

        # test point: verify a results item for each name passed to the API
        assert len(expected) == len(actual), \
            'FAIL: got %s results but expected %s.' \
            % (len(actual), len(expected))

        # loop over the results and validate each name/gender pair
        for i, item in enumerate(actual):

            # test point: verify that we get back the same name that we requested
            assert item[0] == expected[i][0], \
                'expected "%s", but got "%s"' % (expected[i][0], item[0])

            # test point: verify the expected gender for the name
            assert item[1] == expected[i][1], \
                'expected "%s", but got "%s"' % (expected[i][1], item[1])

    def test_int_as_name(self, genderizer):
        """
            Integers are converted to strings by the API.
        """
        api = self.gender_endpoint
        name = 42
        expected_name = '42'

        res = api.get_gender(name, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that we get back the same name that we requested
        actual_name = res.json()['name']
        assert actual_name == expected_name, \
            f"expected '{expected_name}', but got '{actual_name}'."

    @pytest.mark.parametrize('more_than_11_names', [n for n in too_many_names],
                             ids=['+'.join(l[0]) for l in too_many_names])
    def test_exceed_multiple_request_limit(self, genderizer, more_than_11_names):
        """
            Request 11 names in one API call; the limit is 10 so any
            name after the tenth gets ignored.

            :param more_than_11_names: tuple, list of str names and
            list of str genders
            :return: None
        """
        api = self.gender_endpoint
        name = list(more_than_11_names[0])  # needs to be a list
        logger.info(f"\n----> name: {name}")

        res = api.get_gender(name, verbose=True)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # convert the param from list of names + list of genders
        # to list of name + gender pairs
        expected = list(zip(more_than_11_names[0],
                            more_than_11_names[1]))[:10]  # keep list to ten
        logger.info('expected: %s' % expected)

        # convert the returned json into a list of name + gender pairs
        actual = [(n['name'], n['gender']) for n in res.json()]
        logger.info('actual: %s' % actual)

        # test point: verify that the json keys are correct for the first item
        assert api.verify_keys_in_response(res.json()[0].keys())

        # test point: verify a results item for each name passed to the API
        assert len(expected) == len(actual), \
            'FAIL: got %s results but expected %s.' \
            % (len(actual), len(expected))

        # loop over the results and validate each name/gender pair
        for i, item in enumerate(actual):

            # test point: verify that we get back the same name that we requested
            assert item[0] == expected[i][0], \
                'expected "%s", but got "%s"' % (expected[i][0], item[0])

            # test point: verify the expected gender for the name
            assert item[1] == expected[i][1], \
                'expected "%s", but got "%s"' % (expected[i][1], item[1])
