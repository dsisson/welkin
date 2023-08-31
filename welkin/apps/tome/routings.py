# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.tome.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'tome home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'tome product ai page': {
        'module': 'pages',
        'object': 'ProductAiPage',
        'path': NOAUTH_PATH
    },
    'tome product integrations page': {
        'module': 'pages',
        'object': 'ProductIntegrationsPage',
        'path': NOAUTH_PATH
    },
    'tome templates page': {
        'module': 'pages',
        'object': 'TemplatesPage',
        'path': NOAUTH_PATH
    },
    'tome community page': {
        'module': 'pages',
        'object': 'CommunityPage',
        'path': NOAUTH_PATH
    },
    'tome pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
    'tome blog page': {
        'module': 'pages',
        'object': 'BlogPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
