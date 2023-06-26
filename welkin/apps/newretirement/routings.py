# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.newretirement.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'nr home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'nr how-it-works page': {
        'module': 'pages',
        'object': 'HowItWorksPage',
        'path': NOAUTH_PATH
    },
    'nr pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
    'nr blog earning page': {
        'module': 'pages',
        'object': 'BlogEarningPage',
        'path': NOAUTH_PATH
    },
    # 'nr classes page': {
    #     'module': 'pages',
    #     'object': 'ClassesPage',
    #     'path': NOAUTH_PATH
    # },
    'nr apis page': {
        'module': 'pages',
        'object': 'ApisPage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
