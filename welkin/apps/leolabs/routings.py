# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.leolabs.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'leolabs home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'leolabs LeoTrack page': {
        'module': 'pages',
        'object': 'LeotrackPage',
        'path': NOAUTH_PATH
    },
    'leolabs radars page': {
        'module': 'pages',
        'object': 'RadarsPage',
        'path': NOAUTH_PATH
    },
    'leolabs vertex page': {
        'module': 'pages',
        'object': 'VertexPage',
        'path': NOAUTH_PATH
    },
    'leolabs regulators page': {
        'module': 'pages',
        'object': 'RegulatorsPage',
        'path': NOAUTH_PATH
    },
    'leolabs insurers page': {
        'module': 'pages',
        'object': 'InsurersPage',
        'path': NOAUTH_PATH
    },
    'leolabs LeoPulse page': {
        'module': 'pages',
        'object': 'LeoPulsePage',
        'path': NOAUTH_PATH
    },
    'leolabs about us page': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
