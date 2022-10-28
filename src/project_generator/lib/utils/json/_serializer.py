'''
Implementation for JSON serializer
'''
from enum import Enum
from json import JSONEncoder
from re import sub


def _camel_case(input_str: str) -> str:
    '''
    Turn the provided input string into `camelCase`. If the string has delimiters,
    they must be one of '_' or '-'.
    '''
    input_str = sub(r"(_|-)+", " ", input_str).title().replace(" ", "")
    return ''.join([input_str[0].lower(), input_str[1:]])


class TransformType(Enum):
    '''
    Support key name transformations
    '''
    CAMEL_CASE = 0
    SNAKE_CASE = 1
    PASCAL_CASE = 2


class Serializer(JSONEncoder):
    '''
    Custom JSON serializer
    '''

    _enc_list = ['to_json', 'json', 'to_dict']
    _builtin_types = (
        dict, int, list, str, float, tuple, bool)

    def __init__(self, *args, transform_keys: TransformType = None, bypass=False,  ** kw):
        JSONEncoder.__init__(self, *args, **kw)
        self._transform_keys = transform_keys
        self._bypass = bypass

    def default(self, o):
        '''
        Overridden default converter method
        '''
        json_repr = {}

        try:
            json_repr = JSONEncoder.default(self, o)
            return json_repr
        except TypeError:
            pass

        serialize_delegate = None
        if not self._bypass:
            for attr in Serializer._enc_list:
                if hasattr(o, attr):
                    serialize_delegate = getattr(o, attr)
                    break

        if serialize_delegate is not None:
            return serialize_delegate()

        if hasattr(o, '__dict__'):
            print(getattr(o, '__dict__'))
            for k, value in getattr(o, '__dict__'):
                serialized = False

                if self._transform_keys == TransformType.CAMEL_CASE:
                    k = _camel_case(k)

                if isinstance(value, Serializer._builtin_types):
                    json_repr[k] = value
                    serialized = True

                if not serialized and value is not None:
                    json_repr[k] = self.default(value)
        elif hasattr(o, '__slots__'):
            for k in getattr(o, '__slots__'):
                serialized = False

                value = getattr(o, k)

                if self._transform_keys == TransformType.CAMEL_CASE:
                    k = _camel_case(k)

                if isinstance(value, Serializer._builtin_types):
                    json_repr[k] = value
                    serialized = True

                if not serialized and value is not None:
                    json_repr[k] = self.default(value)

        if len(json_repr) == 0:
            return JSONEncoder.default(self, o)

        return json_repr
