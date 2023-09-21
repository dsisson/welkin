# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.cognizant.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'cognizant home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'cognizant automotive page': {
        'module': 'pages',
        'object': 'AutomotivePage',
        'path': NOAUTH_PATH
    },
    'cognizant insurance page': {
        'module': 'pages',
        'object': 'InsurancePage',
        'path': NOAUTH_PATH
    },
    'cognizant enterprise platforms page': {
        'module': 'pages',
        'object': 'EnterprisePlatformsPage',
        'path': NOAUTH_PATH
    },
    'cognizant modern business page': {
        'module': 'pages',
        'object': 'ModernBusinessPage',
        'path': NOAUTH_PATH
    },
    'cognizant annual report page': {
        'module': 'pages',
        'object': 'AnnualReportPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
