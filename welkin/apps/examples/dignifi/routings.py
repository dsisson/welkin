# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.dignifi.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'dignifi home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'dignifi why page': {
        'module': 'pages',
        'object': 'WhyPage',
        'path': NOAUTH_PATH
    },
    'dignifi features and benefits page': {
        'module': 'pages',
        'object': 'FeaturesPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
