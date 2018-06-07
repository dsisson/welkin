""" Test data for genderize API. """

good_names_single = [
    ('Kim', 'female'),
    ('kim', 'female'),
    ('Skyler', 'male'),
    ('Logan', 'male'),
    ('Bob\'s', 'male'),

]


good_names_multiple = [
    (('Bob', 'Joe'), ('male', 'male')),
    (('Bob', 'Joe', 'Sue'), ('male', 'male', 'female')),
    (('Bob', 'Joe', 'Sue', 'Bob'), ('male', 'male', 'female', 'male')),
]


bad_names_single = [
    ' kim',  # initial space
    'smersh',  # not a name
    ' ',  # whitespace
    '<foo>',  # non alpha characters
]


bad_names_multiple = [
    (('Bob', 'Sue', 'smersh'), ('male', 'female', None)),
]


invalid_inputs = [
    (None, 422, "Missing 'name' parameter"),
]


countries = [

]