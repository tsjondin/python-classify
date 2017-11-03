
import inspect
from collections import namedtuple


_PRIMITIVES = frozenset([int, float, str, bool, None])
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
    if model in _PRIMITIVES:
        return _classify_primitive(data, model)

    if inspect.isclass(model):
        for classifier in _registered_classifiers:
            if issubclass(model, classifier.basetype):
                return classifier.to_class(data, model)
        return _classify_instance(data, model)
    else:
        raise TypeError('cannot classify into non-class "{}"'.format(model))


def register(T, classifier):
    """ Registers a classifier for a type, this classifier is used to validate
    whether a simpler representation of a type is representative of the type
    and should return an instance of type T.

    Keyword arguments:
    T -- The type to validate
    classifier -- The function that performs the validation
    """
    _registered_classifiers.add(
        _classifier(basetype=T, to_class=classifier))


def classifier(T):
    """ Decorator version of register, see register(T, classifier) """
    def wrapper(func):
        register(T, func)
    return wrapper


def declassify(model, data):
    """
    !! NOT YET IMPLEMENTED !!

    Delassifies the given *data* from the *model* model/type, any type issue
    will raise TypeError, if no error is raised it will return a python type
    appropriate for the model/class given

    model -- a model (class) to declassify the data from
    data -- a python instance
    """
    pass
