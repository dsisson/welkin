minimal_scenarios = {
    'country': {
        # negative path - empty value
        'empty value': [
            {'nat': ''},
        ],

        # negative path - null value
        'null value': [
            {'nat': None},
        ],

        # # need a way to get a dict w/ dupe keys to not get auto-fixed
        # # negative path - duplicate keys
        # 'duplicate keys, same value': [
        #     {'nat': 'AU', 'nat': 'AU'},
        # ],
        # 
        # # negative path - duplicate keys
        # 'duplicate keys, different values': [
        #     {'nat': 'DE', 'nat': 'AU'},
        # ],

        # not a valid country value
        'au = 1': [
            {'nat': 'au'},
        ],
        '"100" = 1': [
            {'nat': '100'},
        ],
        '100 = 1': [
            {'nat': 100},
        ],
        'grapefruit = 1': [
            {'nat': 'grapefruit'},
        ],

        # simple check
        'AU = 1': [
            {'nat': 'AU'},
        ],

        # ordering of results - alpha?
        'DE = 1, AU = 1': [
            {'nat': 'DE'},
            {'nat': 'AU'},
        ],
        'AU = 1, DE = 1': [
            {'nat': 'AU'},
            {'nat': 'DE'},
        ],

        # ordering of results - by count?
        'AU = 2, DE = 1': [
            {'nat': 'AU'},
            {'nat': 'AU'},
            {'nat': 'DE'},
        ],
        'DE = 1, AU = 2': [
            {'nat': 'DE'},
            {'nat': 'AU'},
            {'nat': 'AU'},
        ],

        # ordering of results from mixed input - by count?
        'AU = 1, DE = 1, AU = 1': [
            {'nat': 'AU'},
            {'nat': 'DE'},
            {'nat': 'AU'},
        ],

    },
    'gender': {
        # negative paths
        'empty value': [
            {'gender': ''},
        ],
        'null value': [
            {'gender': None},
        ],

        # not a valid gender
        'grapefruit': [
            {'gender': 'grapefruit'},
        ],

        # is case normalized?
        'case variations': [
            {'gender': 'FEMAlE'},
            {'gender': 'FemalE'},
            {'gender': 'FeMaLe'},
        ],

        # are leading/trailing spaces normalized?
        'space variations': [
            {'gender': ' female'},
            {'gender': 'female'},
            {'gender': 'female '},
            {'gender': ' female '},
        ],

        # simple check
        'male = 1': [
            {'gender': 'male'},
        ],
        'female = 1': [
            {'gender': 'female'},
        ],

        # counting checks
        'male = 24, female = 26': [
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'male'},
            {'gender': 'female'},
            {'gender': 'female'},
            {'gender': 'female'},
        ],

    },
    'complexity': {
        # negative paths
        'empty value': [
            {'login': {'password': ''}},
        ],
        'null value': [
            {'login': {'password': None}},
        ],
        'empty + null values': [
            {'login': {'password': ''}},
            {'login': {'password': None}},
        ],

        # password variations
        'complexity variations': [
            {'login': {'password': '12'}},
            {'login': {'password': 'a1'}},
            {'login': {'password': 'a1$'}},
            {'login': {'password': 'a1$#'}},
            {'login': {'password': 'a1$_'}},
            {'login': {'password': 'a1$@'}},
            {'login': {'password': 'a1$!'}},
            {'login': {'password': 'a1$&'}},
            {'login': {'password': 'a1$&'}},
            {'login': {'password': 'a1$-'}},
            {'login': {'password': 'a1$ '}},
            {'login': {'password': 'a1$^'}},
            {'login': {'password': 'a1$('}},
            {'login': {'password': 'a1$]'}},
            {'login': {'password': 'a1$/'}},
        ],

    }
}
