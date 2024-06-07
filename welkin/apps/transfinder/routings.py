# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.transfinder.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'transfinder home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'transfinder viewfinder page': {
        'module': 'pages',
        'object': 'ViewfinderPage',
        'path': NOAUTH_PATH
    },
    'transfinder tripfinder page': {
        'module': 'pages',
        'object': 'TripfinderPage',
        'path': NOAUTH_PATH
    },
    'transfinder marketplace page': {
        'module': 'pages',
        'object': 'MarketplacePage',
        'path': NOAUTH_PATH
    },
    'transfinder professional services page': {
        'module': 'pages',
        'object': 'ProfessionalServicesPage',
        'path': NOAUTH_PATH
    },
    'transfinder about us page': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
    'transfinder case studies page': {
        'module': 'pages',
        'object': 'CaseStudiesPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
