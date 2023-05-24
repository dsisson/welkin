# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.polywood.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'polywood home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'polywood categories page': {
        'module': 'pages',
        'object': 'CategoriesPage',
        'path': NOAUTH_PATH
    },
    'polywood collections page': {
        'module': 'pages',
        'object': 'CollectionsPage',
        'path': NOAUTH_PATH
    },
    'polywood get inspired page': {
        'module': 'pages',
        'object': 'GetInspiredPage',
        'path': NOAUTH_PATH
    },
    'polywood designer series page': {
        'module': 'pages',
        'object': 'DesignerSeriesPage',
        'path': NOAUTH_PATH
    },
    'polywood showrooms page': {
        'module': 'pages',
        'object': 'ShowroomsPage',
        'path': NOAUTH_PATH
    },
    'polywood my account page': {
        'module': 'pages',
        'object': 'MyAccountPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
