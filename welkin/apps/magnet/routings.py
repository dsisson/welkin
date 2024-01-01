# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.magnet.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'magnet home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'magnet axiom cyber page': {
        'module': 'pages',
        'object': 'AxiomCyberPage',
        'path': NOAUTH_PATH
    },
    'magnet officer wellness page': {
        'module': 'pages',
        'object': 'OfficerWellnessPage',
        'path': NOAUTH_PATH
    },
    'magnet strategic partners page': {
        'module': 'pages',
        'object': 'StrategicPartnersPage',
        'path': NOAUTH_PATH
    },
    'magnet our story page': {
        'module': 'pages',
        'object': 'OurStoryPage',
        'path': NOAUTH_PATH
    },
    'magnet artifact iq page': {
        'module': 'pages',
        'object': 'ArtifactIQPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
