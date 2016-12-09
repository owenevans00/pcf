from collections import OrderedDict
from products import product_to_business, short_envs

class Pattern:

    # class level list of all supported patterns & fields
    pattern_fields = {
        'Solo' : OrderedDict([
                ('Queue Name', (suggest_queue_name, 'Q')),
                ('Queue Manager', '{qmgr}')
            ]),
        'Alias' : OrderedDict([
                ('Alias Name', (suggest_queue_name, 'A')),
                ('Queue Name', (suggest_queue_name, 'Q')),
                ('Queue Manager', '{qmgr}'),
                ('Cluster', '')
            ]),
        'Point to Point' : OrderedDict([
                ('Remote Queue Name', (suggest_queue_name, 'R')),
                ('Remote Queue Manager', '{qmgr}'),
                ('Local Queue Name', (suggest_queue_name, 'Q')),
                ('Local Queue Manager', '{qmgr}')
            ]),
        'Router' : OrderedDict([
                ('Source Remote Queue Name', (suggest_queue_name, 'R')),
                ('Source Queue Manager', '{qmgr}'),
                ('Destination Remote Queue Name', (suggest_queue_name, 'R')),
                ('Destination Queue Manager', '{qmgr}')
            ]),
        'Server to Client' : OrderedDict([
                ('Queue Manager', '{qmgr}'),
                ('Channel Name', (suggest_channel_name, 'TO')),
                ('SSL CipherSpec', ''),
                ('SSL Peername', '')
        ])
    }

    # eg P.FOO.BAR.{id}.Q
    def suggest_queue_name(product, env, suffix):
        return ('%s.%s.%s.{id}.%s' % (
                    env,
                    product_to_business[product],
                    product,
                    suffix
                ))

    # eg P.FOO.BAR.TO.{id}
    def suggest_channel_name(product, env, direction):
        return ('%s.%s.%s.%s.{id}' % (
                    env,
                    product_to_business[product],
                    product,
                    direction
                ))

    def __init__(self, name, product, env):
        self.name = name
        self.product = product
        self.env = env
        self.pattern_fields = Pattern.pattern_fields[name]

        # go through the fields and invoke suggestion functions
        for k,v in self.pattern_fields.items():
            try:
                f,s = v
                self.pattern_fields[k] = f(product, env, s);
            except ValueError: # not a tuple
                pass
            except TypeError: # f is not a function?
                pass
        
    # factory method in case we need to specialize things later
    def Get(name, product, env): 
            return Pattern(name, product, env)

             