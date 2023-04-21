# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.allergan.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'allergan home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'allergan alle page': {
        'module': 'pages',
        'object': 'AllePage',
        'path': NOAUTH_PATH
    },
    'allergan careers page': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
