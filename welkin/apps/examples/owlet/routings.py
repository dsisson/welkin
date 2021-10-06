# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.owlet.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'owlet home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'owlet smart sock page': {
        'module': 'pages',
        'object': 'SmartSockPage',
        'path': NOAUTH_PATH
    },
    'owlet dream lab page': {
        'module': 'pages',
        'object': 'DreamLabPage',
        'path': NOAUTH_PATH
    },
    'owlet pregnancy band page': {
        'module': 'pages',
        'object': 'PregnancyBandPage',
        'path': NOAUTH_PATH
    },
    'owlet why page': {
        'module': 'pages',
        'object': 'WhyOwletPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
