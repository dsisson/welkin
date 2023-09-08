import pytest
import logging

from welkin.framework import utils
from welkin.apps.census.api import ToyCensusEndpoint
from welkin.apps.census.data.scenarios import minimal_scenarios as minidata

logger = logging.getLogger(__name__)


@pytest.mark.api
class CensusTests(object):

    def test_no_action(self, toycensus):
        # set up API call
        top=0
        users = {'gender': 'female'}
        logger.info(f"\nusers:\n{utils.plog(users)}")
        action_type= ''

        api = ToyCensusEndpoint()
        res = api.get_count(users=users, action_type=action_type, top=top,
                            expect_status=200, expect_errors=False,
                            verbose=True)

        logger.info(f"\nres:\n{utils.plog(res)}")

    def test_invalid_action(self, toycensus):
        # set up API call
        top=0
        users = {'gender': 'female'}
        logger.info(f"\nusers:\n{utils.plog(users)}")
        action_type= 'FooBar'

        api = ToyCensusEndpoint()
        res = api.get_count(users=users, action_type=action_type, top=top,
                            expect_status=200, expect_errors=False,
                            verbose=True)

        logger.info(f"\nres:\n{utils.plog(res)}")

    @pytest.mark.parametrize('country', [
        ['empty value', 0],
        ['null value', 0],
        ['au = 1', 0],
        ['"100" = 1', 0],
        ['100 = 1', 0],
        ['grapefruit = 1', 0],

        ['AU = 1', None],
        ['AU = 1', 0],
        ['AU = 1', 1],
        ['AU = 1', 2],
        ['AU = 1', 10],

        ['DE = 1, AU = 1', None],
        ['DE = 1, AU = 1', 0],
        ['DE = 1, AU = 1', 1],
        ['DE = 1, AU = 1', 2],
        ['DE = 1, AU = 1', 3],
        ['DE = 1, AU = 1', 10],

        ['AU = 1, DE = 1', None],
        ['AU = 1, DE = 1', 0],
        ['AU = 1, DE = 1', 1],
        ['AU = 1, DE = 1', 2],
        ['AU = 1, DE = 1', 3],
        ['AU = 1, DE = 1', 10],

        ['AU = 2, DE = 1', None],
        ['AU = 2, DE = 1', 0],
        ['AU = 2, DE = 1', 1],
        ['AU = 2, DE = 1', 2],
        ['AU = 2, DE = 1', 3],
        ['AU = 2, DE = 1', 4],
        ['AU = 2, DE = 1', 10],

        ['AU = 1, DE = 1, AU = 1', None],
        ['AU = 1, DE = 1, AU = 1', 0],
        ['AU = 1, DE = 1, AU = 1', 1],
        ['AU = 1, DE = 1, AU = 1', 2],
        ['AU = 1, DE = 1, AU = 1', 3],
        ['AU = 1, DE = 1, AU = 1', 4],
        ['AU = 1, DE = 1, AU = 1', 10],

    ])
    def test_minimal_country(self, toycensus, country):
        # unpack parameter
        key, top = country
        users = minidata['country'][key]
        logger.info(f"\nusers:\n{utils.plog(users)}")

        # set up API call
        action_type= 'CountByCountry'
        api = ToyCensusEndpoint()
        res = api.get_count(users=users, action_type=action_type, top=top,
                            expect_status=200, expect_errors=False,
                            verbose=True)

        logger.info(f"\nres.json():\n{utils.plog(res.json())}")

        # test point: verify that the json keys are correct
        # using the older keys expected_keys approach
        for item in res.json():
            assert api.verify_keys_in_response(item.keys(), verbose=True)

    @pytest.mark.parametrize('gender', [
        ['empty value', 0],
        ['null value', 0],
        ['grapefruit', 0],
        ['case variations', 0],
        ['space variations', 0],

        ['male = 1', 0],
        ['female = 1', 0],
        ['male = 24, female = 26', 0],
        ['male = 24, female = 26', 1],
        ['male = 24, female = 26', 2],
        ['male = 24, female = 26', 3],
        ['male = 24, female = 26', 4],
        ['male = 24, female = 26', 5],

    ])
    def test_minimal_gender(self, toycensus, gender):
        # unpack parameter
        key, top = gender
        users = minidata['gender'][key]
        logger.info(f"\nusers:\n{utils.plog(users)}")

        # set up API call
        action_type= 'CountByGender'
        api = ToyCensusEndpoint()
        res = api.get_count(users=users, action_type=action_type, top=top,
                            expect_status=200, expect_errors=False,
                            verbose=True)

        logger.info(f"\nres.json():\n{utils.plog(res.json())}")

        # test point: verify that the json keys are correct
        # using the older keys expected_keys approach
        for item in res.json():
            assert api.verify_keys_in_response(item.keys(), verbose=True)

    @pytest.mark.parametrize('complexity', [
        ['empty value', 0],
        ['null value', 0],
        ['empty + null values', 0],

        ['complexity variations', 0],
        ['complexity variations', 1],
        ['complexity variations', 2],
        ['complexity variations', 3],
        ['complexity variations', 4],
        ['complexity variations', 10],
        ['complexity variations', 11],
        ['complexity variations', 12],
        ['complexity variations', 13],
        ['complexity variations', 14],
        ['complexity variations', 15],
        ['complexity variations', 16],

    ])
    def test_minimal_pwcomplexity(self, toycensus, complexity):
        # unpack parameter
        key, top = complexity
        users = minidata['complexity'][key]
        logger.info(f"\nusers:\n{utils.plog(users)}")

        # set up API call
        action_type= 'CountPasswordComplexity'
        api = ToyCensusEndpoint()
        res = api.get_count(users=users, action_type=action_type, top=top,
                            expect_status=200, expect_errors=False,
                            verbose=True)

        logger.info(f"\nres.json():\n{utils.plog(res.json())}")

        # test point: verify that the json keys are correct
        # using the older keys expected_keys approach
        for item in res.json():
            assert api.verify_keys_in_response(item.keys(), verbose=True)

