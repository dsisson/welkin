# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.cb.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'cb home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'cb about page': {
        'module': 'pages',
        'object': 'AboutPage',
        'path': NOAUTH_PATH
    },
    'cb history page': {
        'module': 'pages',
        'object': 'HistoryPage',
        'path': NOAUTH_PATH
    },
    'cb how it works page': {
        'module': 'pages',
        'object': 'HowItWorksPage',
        'path': NOAUTH_PATH
    },
    'cb start a site page': {
        'module': 'pages',
        'object': 'StartASitePage',
        'path': NOAUTH_PATH
    },
    'cb resources page': {
        'module': 'pages',
        'object': 'ResourcesPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
