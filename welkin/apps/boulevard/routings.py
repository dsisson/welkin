# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.boulevard.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'boulevard home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'boulevard salon page': {
        'module': 'pages',
        'object': 'SalonPage',
        'path': NOAUTH_PATH
    },
    'boulevard owners page': {
        'module': 'pages',
        'object': 'OwnersPage',
        'path': NOAUTH_PATH
    },
    'boulevard features page': {
        'module': 'pages',
        'object': 'FeaturesPage',
        'path': NOAUTH_PATH
    },
    'boulevard self-booking page': {
        'module': 'pages',
        'object': 'SelfBookingPage',
        'path': NOAUTH_PATH
    },
    'boulevard contact center page': {
        'module': 'pages',
        'object': 'ContactCenterPage',
        'path': NOAUTH_PATH
    },
    'boulevard blog page': {
        'module': 'pages',
        'object': 'BlogPage',
        'path': NOAUTH_PATH
    },
    'boulevard success stories page': {
        'module': 'pages',
        'object': 'SuccessStoriesPage',
        'path': NOAUTH_PATH
    },
    'boulevard our story page': {
        'module': 'pages',
        'object': 'OurStoryPage',
        'path': NOAUTH_PATH
    },
    'boulevard customer love page': {
        'module': 'pages',
        'object': 'CustomerLovePage',
        'path': NOAUTH_PATH
    },
    'boulevard pricing page': {
        'module': 'pages',
        'object': 'PricingPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
