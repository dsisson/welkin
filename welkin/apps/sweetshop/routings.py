# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.sweetshop.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': 'welkin.apps.sweetshop.'
    },

    'sweetshop home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'sweetshop sweets page': {
        'module': 'pages',
        'object': 'SweetsPage',
        'path': NOAUTH_PATH
    },
    'sweetshop about page': {
        'module': 'pages',
        'object': 'AboutPage',
        'path': NOAUTH_PATH
    },
    'sweetshop login page': {
        'module': 'pages',
        'object': 'LoginPage',
        'path': NOAUTH_PATH
    },
    'sweetshop basket page': {
        'module': 'pages',
        'object': 'BasketPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
