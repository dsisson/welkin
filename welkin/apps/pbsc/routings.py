# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.pbsc.noauth.'
AUTH_PATH = None  # not implemented for this wrapper


# mapping page object names to classes
noauth_pageobjects = {
    'pbsc home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'pbsc product salsa page': {
        'module': 'pages',
        'object': 'ProductSalsaPage',
        'path': NOAUTH_PATH
    },
    'pbsc product quac & chips booth page': {
        'module': 'pages',
        'object': 'ProductGuacChipsBoothPage',
        'path': NOAUTH_PATH
    },
    'pbsc product salsa software page': {
        'module': 'pages',
        'object': 'ProductSalsaSoftwarePage',
        'path': NOAUTH_PATH
    },
    'pbsc pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
    'pbsc start a business guide page': {
        'module': 'pages',
        'object': 'GuideStartBusinessPage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
