# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.arcticwolf.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'arcticwolf home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'arcticwolf solutions page': {
        'module': 'pages',
        'object': 'SolutionsPage',
        'path': NOAUTH_PATH
    },
    'arcticwolf how it works page': {
        'module': 'pages',
        'object': 'HowItWorksPage',
        'path': NOAUTH_PATH
    },
    'arcticwolf why page': {
        'module': 'pages',
        'object': 'WhyPage',
        'path': NOAUTH_PATH
    },
    'arcticwolf resource center page': {
        'module': 'pages',
        'object': 'ResourceCenterPage',
        'path': NOAUTH_PATH
    },
    'arcticwolf partners providers page': {
        'module': 'pages',
        'object': 'PartnersProvidersPage',
        'path': NOAUTH_PATH
    },
    'arcticwolf company leadership page': {
        'module': 'pages',
        'object': 'CompanyLeadershipPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
