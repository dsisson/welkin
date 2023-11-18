# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.cyware.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'cyware home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'cyware intel exchange lite page': {
        'module': 'pages',
        'object': 'IntelExchangeLitePage',
        'path': NOAUTH_PATH
    },
    'cyware orchestrate page': {
        'module': 'pages',
        'object': 'OrchestratePage',
        'path': NOAUTH_PATH
    },
    'cyware open apis page': {
        'module': 'pages',
        'object': 'OpenApisPage',
        'path': NOAUTH_PATH
    },
    'cyware security guides page': {
        'module': 'pages',
        'object': 'SecurityGuidesPage',
        'path': NOAUTH_PATH
    },
    'cyware compliance page': {
        'module': 'pages',
        'object': 'CompliancePage',
        'path': NOAUTH_PATH
    },
    'cyware blog page': {
        'module': 'pages',
        'object': 'BlogPage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
