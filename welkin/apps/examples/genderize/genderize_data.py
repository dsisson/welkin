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
    (('Bob', 'Joe', 'Sue', 'Spencer'), ('male', 'male', 'female', 'male')),
    (  # 10 is the upper limit for names in one request
        ('Bob', 'Joe', 'Sue', 'Spencer', 'Steve', 'John', 'Mary', 'Jane', 'Henry', 'Juan'),
        ('male', 'male', 'female', 'male', 'male', 'male', 'female', 'female', 'male', 'male')
    ),
]


bad_names_single = [
    ' kim',  # initial space
    'blahxx',  # not a name
    ' ',  # whitespace
    '<foo>',  # non alpha characters
]


bad_names_multiple = [
    (('Bob', 'Sue', 'blahxx'), ('male', 'female', None)),
]

too_many_names = [
    (  # 11 names should return error
        ('Bob', 'Joe', 'Sue', 'Spencer', 'Steve', 'John', 'Mary', 'Jane', 'Henry', 'Juan', 'Pat'),
        ('male', 'male', 'female', 'male', 'male', 'male', 'female', 'female', 'male', 'male', 'male')
    ),

]

invalid_inputs = [
    (None, 422, "Missing 'name' parameter"),
]


countries = [

]