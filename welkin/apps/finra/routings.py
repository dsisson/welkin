# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.finra.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'finra home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'finra about page': {
        'module': 'pages',
        'object': 'AboutPage',
        'path': NOAUTH_PATH
    },
    'finra careers page': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
    'finra media center page': {
        'module': 'pages',
        'object': 'MediaCenterPage',
        'path': NOAUTH_PATH
    },
    'finra firm hub page': {
        'module': 'pages',
        'object': 'FirmHubPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
