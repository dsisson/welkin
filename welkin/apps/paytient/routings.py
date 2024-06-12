# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.paytient.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'paytient home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'paytient employers page': {
        'module': 'pages',
        'object': 'EmployersPage',
        'path': NOAUTH_PATH
    },
    'paytient insurers page': {
        'module': 'pages',
        'object': 'InsurersPage',
        'path': NOAUTH_PATH
    },
    'paytient start page': {
        'module': 'pages',
        'object': 'StartPage',
        'path': NOAUTH_PATH
    },
    'paytient what is HPA page': {
        'module': 'pages',
        'object': 'HPAPage',
        'path': NOAUTH_PATH
    },
    'paytient blog page': {
        'module': 'pages',
        'object': 'BlogPage',
        'path': NOAUTH_PATH
    },
    'paytient guides page': {
        'module': 'pages',
        'object': 'GuidesPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
