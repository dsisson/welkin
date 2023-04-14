# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.allstate.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'allstate home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'AIP login page': {
        'module': 'pages',
        'object': 'AppLoginPage',
        'path': NOAUTH_PATH
    },
    'AIP forgot password page': {
        'module': 'pages',
        'object': 'AppForgotPasswordPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
