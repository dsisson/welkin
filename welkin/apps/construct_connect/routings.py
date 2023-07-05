# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.construct_connect.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'construct home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'construct subcontractors page': {
        'module': 'pages',
        'object': 'SubcontractorsPage',
        'path': NOAUTH_PATH
    },
    'construct general contractors page': {
        'module': 'pages',
        'object': 'GeneralContractorsPage',
        'path': NOAUTH_PATH
    },
    'construct bid center page': {
        'module': 'pages',
        'object': 'BidCenterPage',
        'path': NOAUTH_PATH
    },
    'construct survival kit page': {
        'module': 'pages',
        'object': 'SurvivalKitPage',
        'path': NOAUTH_PATH
    },
    'construct careers page': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
