
from classify.classify import classify


class _TypedList:
    pass


def typedlist(T):
    """
    Creates a new typed list type
    """
    return type('List<' + T.__name__ + '>', (_TypedList,), dict(basetype=T))


def classify_list(data, T):
    listed = []
    for value in data:
        member = classify(value, T.basetype)
        listed.append(member)
    return listed
