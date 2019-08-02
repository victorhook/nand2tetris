TYPE = 'int', 'char', 'boolean'


def get(*args):

    for arg in args:
        if arg == TYPE:
            for _type in arg:
                print(_type)

get(TYPE)