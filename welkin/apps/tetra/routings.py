# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.tetra.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'tetra home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'tetra why page': {
        'module': 'pages',
        'object': 'WhyPage',
        'path': NOAUTH_PATH
    },
    'tetra data replatforming page': {
        'module': 'pages',
        'object': 'DataReplatformingPage',
        'path': NOAUTH_PATH
    },
    'tetra quality page': {
        'module': 'pages',
        'object': 'QualityPage',
        'path': NOAUTH_PATH
    },
    'tetra data page': {
        'module': 'pages',
        'object': 'TetraDataPage',
        'path': NOAUTH_PATH
    },
    'tetra flow cytometry page': {
        'module': 'pages',
        'object': 'FlowCytometryPage',
        'path': NOAUTH_PATH
    },
    'tetra newsroom page': {
        'module': 'pages',
        'object': 'NewsroomPage',
        'path': NOAUTH_PATH
    },
}

auth_pageobjects = None  # not implemented for this wrapper
