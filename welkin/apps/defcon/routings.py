# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.defcon.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'defcon home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'defcon mission page': {
        'module': 'pages',
        'object': 'MissionPage',
        'path': NOAUTH_PATH
    },
    'defcon team page': {
        'module': 'pages',
        'object': 'TeamPage',
        'path': NOAUTH_PATH
    },
    'defcon capabilities page': {
        'module': 'pages',
        'object': 'CapabilitiesPage',
        'path': NOAUTH_PATH
    },
    'defcon news page': {
        'module': 'pages',
        'object': 'NewsPage',
        'path': NOAUTH_PATH
    },
    'defcon careers page': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
    'defcon contact us page': {
        'module': 'pages',
        'object': 'ContactUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
