# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.iodine.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'iodine home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'iodine why page': {
        'module': 'pages',
        'object': 'WhyIodinePage',
        'path': NOAUTH_PATH
    },
    'iodine aware cdi page': {
        'module': 'pages',
        'object': 'AwareCdiPage',
        'path': NOAUTH_PATH
    },
    'iodine interact page': {
        'module': 'pages',
        'object': 'InteractPage',
        'path': NOAUTH_PATH
    },
    'iodine cognitiveml page': {
        'module': 'pages',
        'object': 'CognitiveMlPage',
        'path': NOAUTH_PATH
    },
    'iodine chartwise page': {
        'module': 'pages',
        'object': 'ChartwisePage',
        'path': NOAUTH_PATH
    },
    'iodine news insights page': {
        'module': 'pages',
        'object': 'NewsInsightsPage',
        'path': NOAUTH_PATH
    },
    'iodine about page': {
        'module': 'pages',
        'object': 'AboutPage',
        'path': NOAUTH_PATH
    },
    'iodine partnerships page': {
        'module': 'pages',
        'object': 'PartnershipsPage',
        'path': NOAUTH_PATH
    },
    'iodine contact us page': {
        'module': 'pages',
        'object': 'ContactUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
