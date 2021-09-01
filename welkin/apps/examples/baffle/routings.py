# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.baffle.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'baffle home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'baffle data protection services page': {
        'module': 'pages',
        'object': 'DataProtectionPage',
        'path': NOAUTH_PATH
    },
    'baffle solutions overview page': {
        'module': 'pages',
        'object': 'SolutionsOverviewPage',
        'path': NOAUTH_PATH
    },
    'baffle resources overview page': {
        'module': 'pages',
        'object': 'ResourcesOverviewPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
