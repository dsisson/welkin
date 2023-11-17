# path to the no-authentication modules
NOAUTH_PATH = 'welkin.apps.earnest.noauth.'
AUTH_PATH = None  # not implemented for this wrapper

# mapping page object names to classes
noauth_pageobjects = {
    'earnest home page': {
        'module': 'pages',
        'object': 'HomePage',
        'path': NOAUTH_PATH
    },

    'earnest student loans page': {
        'module': 'pages',
        'object': 'StudentLoansPage',
        'path': NOAUTH_PATH
    },
    'earnest parent loans page': {
        'module': 'pages',
        'object': 'ParentLoansPage',
        'path': NOAUTH_PATH
    },
    'earnest resources page': {
        'module': 'pages',
        'object': 'ResourcesPage',
        'path': NOAUTH_PATH
    },
    'earnest refinance student loans page': {
        'module': 'pages',
        'object': 'RefinanceStudentLoansPage',
        'path': NOAUTH_PATH
    },
    'earnest student loan manager page': {
        'module': 'pages',
        'object': 'StudentLoanManagerPage',
        'path': NOAUTH_PATH
    },
    'earnest debt-to-income calculator page': {
        'module': 'pages',
        'object': 'CalculatorDebtIncomePage',
        'path': NOAUTH_PATH
    },

}

auth_pageobjects = None  # not implemented for this wrapper
