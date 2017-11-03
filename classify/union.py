
from classify.classify import classify


class _Union:
    pass


def union(*args):
    """
    Creates a Union of multiple type, one of which the data provided has to
    conform with

    Only used to check instanceof, otherwise it is a pure frozenset

    types - The types of which the data must be one of
    """
    return type(
        'Union<' + ' | '.join(map(lambda a: a.__name__, args)) + '>',
        (_Union,), dict(types=args))


def classify_union(data, u):
    for T in u.types:
        try:
            return classify(data, T)
        except TypeError as e:
            pass
    raise TypeError('Data {} did not match any type in {}'.format(data, u))
