# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.cerebral.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'cerebral home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'cerebral therapy plan page': {
        'module': 'pages',
        'object': 'TherapyPage',
        'path': NOAUTH_PATH
    },
    'cerebral medication therapy plan page': {
        'module': 'pages',
        'object': 'MedicationTherapyPage',
        'path': NOAUTH_PATH
    },
    'cerebral faq page': {
        'module': 'pages',
        'object': 'FaqPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
