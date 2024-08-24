# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.affinipay.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'affinipay home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'affinipay about us page': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
    'affinipay industry perspective page': {
        'module': 'pages',
        'object': 'IndustryPerspectivePage',
        'path': NOAUTH_PATH
    },
    'affinipay careers page': {
        'module': 'pages',
        'object': 'CareersPage',
        'path': NOAUTH_PATH
    },
    'affinipay newsroom page': {
        'module': 'pages',
        'object': 'NewsroomPage',
        'path': NOAUTH_PATH
    },
    'affinipay contact us page': {
        'module': 'pages',
        'object': 'ContactUsPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
