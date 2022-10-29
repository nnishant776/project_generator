'''
Implementation for JSON serializer
'''

from enum import Enum
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


class Serializer:
    '''
    Custom recursive serializer
    '''

    _enc_list = ['to_dict', 'serialize']
    _builtin_types = (int, str, float, bool)
    _iterable_types = (list, tuple)
    _associative_types = (dict, )

    def default(self, obj, bypass=False):
        '''
        Default implementation of the serializer
        '''

        for typ in Serializer._builtin_types:
            if isinstance(obj, typ):
                return obj

        for typ in Serializer._iterable_types:
            if isinstance(obj, typ):
                iter_repr = []
                for val in iter(obj):
                    if val is None:
                        continue
                    iter_repr.append(self.default(val))

                return iter_repr

        for typ in Serializer._associative_types:
            if isinstance(obj, typ):
                assoc_repr = {}
                for key in iter(obj):
                    val = obj[key]
                    if val is None:
                        continue
                    assoc_repr[key] = self.default(val)

                return assoc_repr

        dict_repr = {}

        serialize_delegate = None
        if not bypass:
            for attr in Serializer._enc_list:
                if hasattr(obj, attr):
                    serialize_delegate = getattr(obj, attr)
                    break

        if serialize_delegate is not None:
            return serialize_delegate()

        if hasattr(obj, '__dict__'):
            for k, value in getattr(obj, '__dict__'):
                if value is None:
                    continue
                if isinstance(value, Serializer._builtin_types):
                    dict_repr[k] = value
                else:
                    dict_repr[k] = self.default(value)
        elif hasattr(obj, '__slots__'):
            for k in getattr(obj, '__slots__'):
                value = getattr(obj, k)
                if value is None:
                    continue
                if isinstance(value, Serializer._builtin_types):
                    dict_repr[k] = value
                else:
                    dict_repr[k] = self.default(value)

        return dict_repr
