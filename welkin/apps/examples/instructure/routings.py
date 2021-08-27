# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.instructure.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'instructure home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'instructure k12 page': {
        'module': 'pages',
        'object': 'K12Page',
        'path': NOAUTH_PATH
    },
    'instructure higher education page': {
        'module': 'pages',
        'object': 'HigherEducationPage',
        'path': NOAUTH_PATH
    },
    'instructure news & events page': {
        'module': 'pages',
        'object': 'NewsEventsPage',
        'path': NOAUTH_PATH
    },
    'instructure about us page': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
