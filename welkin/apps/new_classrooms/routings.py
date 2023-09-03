# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.new_classrooms.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'nc home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'nc why we exist page': {
        'module': 'pages',
        'object': 'WhyWeExistPage',
        'path': NOAUTH_PATH
    },
    'nc solution development page': {
        'module': 'pages',
        'object': 'SolutionDevelopmentPage',
        'path': NOAUTH_PATH
    },
    'nc policy page': {
        'module': 'pages',
        'object': 'PolicyPage',
        'path': NOAUTH_PATH
    },
    'nc history page': {
        'module': 'pages',
        'object': 'HistoryPage',
        'path': NOAUTH_PATH
    },
    'nc leadership page': {
        'module': 'pages',
        'object': 'LeadershipPage',
        'path': NOAUTH_PATH
    },
    'nc latest page': {
        'module': 'pages',
        'object': 'LatestPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
