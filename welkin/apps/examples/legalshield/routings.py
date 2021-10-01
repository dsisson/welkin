# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.legalshield.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'legalshield home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'legalshield mission page': {
        'module': 'pages',
        'object': 'MissionPage',
        'path': NOAUTH_PATH
    },
    'legalshield how it works page': {
        'module': 'pages',
        'object': 'HowItWorksPage',
        'path': NOAUTH_PATH
    },
    'legalshield personal plan details page': {
        'module': 'pages',
        'object': 'PersonalPlanDetailsPage',
        'path': NOAUTH_PATH
    },
    'legalshield start a business overview page': {
        'module': 'pages',
        'object': 'StartBusinessOverviewPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
