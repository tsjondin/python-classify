from classify.classify import _get_metatype, _classify_instance, classify, classifier, register # flake8: noqa
from classify.union import _Union, classify_union, union # flake8: noqa
from classify.intersection import _Intersection, intersection # flake8: noqa
from classify.typedlist import _TypedList, classify_list, typedlist # flake8: noqa
from enum import Enum


@classifier(Enum)
def _classify_enum(data, T):
    if not isinstance(data, str) and not isinstance(data, int):
        raise TypeError(
            'Can only classify as Enum using key strings or int values')
    for name, value in vars(T).items():
        print(name, value)
        if name == data:
            return value
        elif value == data:
            return value
    raise TypeError('Invalid key/value {} for Enum {}'.format(data, T))


register(_Union, classify_union)
register(_TypedList, classify_list)
