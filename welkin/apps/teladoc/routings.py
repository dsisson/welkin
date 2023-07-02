# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.teladoc.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'teladoc home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'teladoc expert primary care page': {
        'module': 'pages',
        'object': 'ExpertPrimaryCarePage',
        'path': NOAUTH_PATH
    },
    'teladoc expert speciality care page': {
        'module': 'pages',
        'object': 'ExpertSpecialtyCarePage',
        'path': NOAUTH_PATH
    },
    'teladoc care for adults page': {
        'module': 'pages',
        'object': 'AdultCarePage',
        'path': NOAUTH_PATH
    },
    'teladoc orgs hospital virtual care platform page': {
        'module': 'pages',
        'object': 'OrgsHospitalsVirtualCarePlatformPage',
        'path': NOAUTH_PATH
    },
    'teladoc orgs health plans mental health page': {
        'module': 'pages',
        'object': 'OrgsHealthPlansMentalHealthPage',
        'path': NOAUTH_PATH
    },
    'teladoc orgs employers chronic care page': {
        'module': 'pages',
        'object': 'OrgsEmployersChronicCarePage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
