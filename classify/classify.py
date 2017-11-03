
import inspect
from collections import namedtuple
from enum import Enum


PRIMITIVES = frozenset([int, float, str, bool, None])
_classifier = namedtuple('Classifier', ['basetype', 'to_class'])
_registered_classifiers = set([])


def _get_metatype(T):
    metatype = {}
    for member in dir(T):
        if not member.startswith('_'):
            value = getattr(T, member)
            if (inspect.isclass(value)):
                metatype[member] = value
    return metatype


def _classify_primitive(data, T):
    if T is None and data is not None:
        raise TypeError(
            'Type mismatch {} is not of type None'.format(
                data))
    elif ((T is not None) and
          (not isinstance(data, T)) or
          (T is not bool and
           isinstance(data, bool) and isinstance(data, int))):
        raise TypeError(
            'Type mismatch {} is not of type {}'.format(
                data, T))
    return data


def _classify_instance(data, T):
    """
    Internal function that instantiates type classes and assigns members while
    typecheking them, it returns an instance of T

    data -- data to assign
    T -- type to instantiate
    """
    instance = T()
    metatype = _get_metatype(T)
    for key, item_type in metatype.items():
        if hasattr(instance, key):
            setattr(instance, key, classify(data.get(key, None), item_type))
        else:
            raise TypeError('Type does not have attribute {}'.format(key))
    return instance


def classify(data, model):
    """
    Classifies the given *data* as the *model* type, any type issue will raise
    TypeError, if no error is raised it will return an instance of the
    type/model given as the *model*

    Keyword arguments:
    data -- a python datastructure, such as dict, list etc.
    model -- a model (class) to classify the data as
    """
    if model in PRIMITIVES:
        return _classify_primitive(data, model)

    if inspect.isclass(model):
        for classifier in _registered_classifiers:
            if issubclass(model, classifier.basetype):
                return classifier.to_class(data, model)
        return _classify_instance(data, model)
    else:
        raise TypeError('cannot classify into non-class "{}"'.format(model))


def register(T, func):
    _registered_classifiers.add(
        _classifier(basetype=T, to_class=func))

def classifier(T):
    def wrapper(func):
        register(T, func)
    return wrapper


def declassify(model, data):
    """
    Delassifies the given *data* from the *model* model/type, any type issue
    will raise TypeError, if no error is raised it will return a python type
    appropriate for the model/class given

    model - a model (class) to declassify the data from

    data - a python instance
    """
    pass


@classifier(Enum)
def _classify_enum(data, T):
    if not isinstance(data, str) and not isinstance(data, int):
        raise TypeError('Can only classify as Enum using key strings or int values')
    for name, value in vars(T).items():
        if name == data:
            return value
        elif value == data:
            return value
    raise TypeError('Invalid key/value for Enum {}'.format(T))
