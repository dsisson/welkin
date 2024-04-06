# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.clari.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'clari home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'clari why page': {
        'module': 'pages',
        'object': 'WhyPage',
        'path': NOAUTH_PATH
    },
    'clari products capture page': {
        'module': 'pages',
        'object': 'ProductsCapturePage',
        'path': NOAUTH_PATH
    },
    'clari products groove page': {
        'module': 'pages',
        'object': 'ProductsGroovePage',
        'path': NOAUTH_PATH
    },
    'clari solutions usecases page': {
        'module': 'pages',
        'object': 'SolutionsUsecasesPage',
        'path': NOAUTH_PATH
    },
    'clari pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
