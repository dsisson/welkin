# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.duckduckgo.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'duckduckgo external home page': {
        'module': 'pages',
        'object': 'ExternalHomePage',
        'path': NOAUTH_PATH
    },
    'duckduckgo internal home page': {
        'module': 'pages',
        'object': 'InternalHomePage',
        'path': NOAUTH_PATH
    },
    'duckduckgo search results page': {
        'module': 'pages',
        'object': 'SearchResultsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
