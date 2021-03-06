
from classify.classify import _get_definition


class _Intersection:
    pass


def intersection(*args):
    """
    Creates an Intersection of multiple unique types that the data provided
    has to conform with.

    Only used to check instanceof, otherwise it is a pure frozenset

    types - The types to expect an intersection of
    """
    prototype = {}
    for T in args:
        prototype.update(_get_definition(T))
    return type(
        'Intersection<' + ' & '.join(map(lambda a: a.__name__, args)) + '>',
        (_Intersection,), prototype)
