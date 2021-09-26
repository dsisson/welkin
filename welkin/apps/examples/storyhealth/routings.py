# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.examples.storyhealth.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'storyhealth home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'storyhealth mission': {
        'module': 'pages',
        'object': 'MissionPage',
        'path': NOAUTH_PATH
    },
    'storyhealth about us': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
    'storyhealth careers': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
    'storyhealth contact us': {
        'module': 'pages',
        'object': 'ContactUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
