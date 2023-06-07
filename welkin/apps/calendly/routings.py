# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.calendly.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'calendly home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'calendly products page': {
        'module': 'pages',
        'object': 'ProductsPage',
        'path': NOAUTH_PATH
    },
    'calendly solutions page': {
        'module': 'pages',
        'object': 'SolutionsPage',
        'path': NOAUTH_PATH
    },
    'calendly teams & companies page': {
        'module': 'pages',
        'object': 'TeamsCompaniesPage',
        'path': NOAUTH_PATH
    },
    'calendly pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
    'calendly resources page': {
        'module': 'pages',
        'object': 'ResourcesPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
