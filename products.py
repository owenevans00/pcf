from collections import OrderedDict

product_to_business = {
    'CANS' : 'DL',
    'GWY' : 'BCI',
    'TSF' : 'TS',
    'OPEN' : 'AIM'
    }

environments = OrderedDict([
    ('P', 'Production'),
    ('B', 'Beta'),
    ('U', 'UAT'),
    ('Q', 'QA')
])

short_envs = {
    'P' : 'PROD',
    'B' : 'BETA',
    'U' : 'UAT',
    'Q' : 'QA'
}