# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.salesloft.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'salesloft home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'salesloft conversations page': {
        'module': 'pages',
        'object': 'ConversationsPage',
        'path': NOAUTH_PATH
    },
    'salesloft deals page': {
        'module': 'pages',
        'object': 'DealsPage',
        'path': NOAUTH_PATH
    },
    'salesloft webinars page': {
        'module': 'pages',
        'object': 'WebinarsPage',
        'path': NOAUTH_PATH
    },
    'salesloft content hub page': {
        'module': 'pages',
        'object': 'ContentHubPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
