# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.zerofox.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'zf home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'zf protection page': {
        'module': 'pages',
        'object': 'ProtectionPage',
        'path': NOAUTH_PATH
    },
    'zf platform page': {
        'module': 'pages',
        'object': 'PlatformPage',
        'path': NOAUTH_PATH
    },
    'zf intelligence page': {
        'module': 'pages',
        'object': 'IntelligencePage',
        'path': NOAUTH_PATH
    },
    'zf partners page': {
        'module': 'pages',
        'object': 'PartnersPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
