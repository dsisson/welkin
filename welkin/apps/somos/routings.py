# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.somos.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'somos home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'somos fraud mitigation page': {
        'module': 'pages',
        'object': 'FraudMitigationPage',
        'path': NOAUTH_PATH
    },
    'somos routing data page': {
        'module': 'pages',
        'object': 'RoutingDataPage',
        'path': NOAUTH_PATH
    },
    'somos about page': {
        'module': 'pages',
        'object': 'AboutPage',
        'path': NOAUTH_PATH
    },
    'somos our team page': {
        'module': 'pages',
        'object': 'OurTeamPage',
        'path': NOAUTH_PATH
    },
    'somos insights page': {
        'module': 'pages',
        'object': 'InsightsPage',
        'path': NOAUTH_PATH
    },
    'somos events page': {
        'module': 'pages',
        'object': 'EventsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
