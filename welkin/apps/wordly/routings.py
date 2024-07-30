# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.wordly.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'POM boot page': {
        'module': 'base_page',
        'object': 'PomBootPage',
        'path': NOAUTH_PATH
    },

    'wordly home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },
    'wordly ai captioning page': {
        'module': 'pages',
        'object': 'AiCaptioningPage',
        'path': NOAUTH_PATH
    },
    'wordly meeting translation page': {
        'module': 'pages',
        'object': 'MeetingTranslationPage',
        'path': NOAUTH_PATH
    },
    'wordly all use cases page': {
        'module': 'pages',
        'object': 'AllUseCasesPage',
        'path': NOAUTH_PATH
    },
    'wordly about us page': {
        'module': 'pages',
        'object': 'AboutUsPage',
        'path': NOAUTH_PATH
    },
    'wordly why page': {
        'module': 'pages',
        'object': 'WhyWordlyPage',
        'path': NOAUTH_PATH
    },
    'wordly how wordly works page': {
        'module': 'pages',
        'object': 'HowWordlyWorksPage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
