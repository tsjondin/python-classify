
import inspect
from collections import namedtuple


_PRIMITIVES = frozenset([int, float, str, bool, None])
_classifier = namedtuple('Classifier', ['basetype', 'to_class'])
_registered_classifiers = set([])


def _get_definition(model):
    definition = {}
    for member in dir(model):
        if not member.startswith('_'):
            value = getattr(model, member)
            if (inspect.isclass(value)):
                definition[member] = value
    return definition


def _classify_primitive(data, model):
    if model is None and data is not None:
        raise TypeError(
            'Type mismatch {} is not of type None'.format(
                data))
    elif ((model is not None) and (not isinstance(data, model)) or
          ((model is not bool) and isinstance(data, bool) and
           isinstance(data, int))):
        raise TypeError('Type mismatch {} is not of type {}'.format(
            data,
            model.__name__))
    return data


def _classify_instance(data, model):
    """
    Internal function that instantiates type classes and assigns members while
    typecheking them, it returns an instance of model

    **Keyword arguments**:

    * data -- data to assign
    * model -- type to instantiate
    """
    try:
        instance = model()
    except Exception as e:
        raise TypeError(
            'Could not instantiate Type {}, is this a proper classify ' +
            'model or is it a Type in need of a classifier?'.format(
                model.__name__))
    definition = _get_definition(model)
    expected = set(definition.keys())
    checked = set([])
    for key, value in data.items():
        if hasattr(instance, key):
            setattr(instance, key, classify(definition.get(key, type(None)), value))
            checked.add(key)
        else:
            raise TypeError('Type {} does not have attribute {}'.format(
                model.__name__, key))
    if not checked <= expected:
        raise TypeError('Type {} expected attribute {}'.format(
            model.__name__, ', '.join(expected)))
    return instance


def classify(model, data):
    """
    Classifies the given *data* as the *model* type, any type issue will raise
    TypeError, if no error is raised it will return an instance of the
    type/model given as the *model*

    **Keyword arguments**:

    * model -- a model (class) to classify the data as
    * data -- a python datastructure, such as dict, list etc.
    """
    if model in _PRIMITIVES:
        return _classify_primitive(data, model)

    if inspect.isclass(model):
        for classifier in _registered_classifiers:
            if issubclass(model, classifier.basetype):
                return classifier.to_class(data, model)
        return _classify_instance(data, model)
    else:
        raise TypeError('Invalid argument {} is not a type-model'.format(
            model))


def register(model, classifier):
    """
    Registers a classifier for a type, this classifier is used to validate
    whether a simpler representation of a type is representative of the type
    and should return an instance of type model.

    **Keyword arguments**:

    * model -- The type to validate
    * classifier -- The function that performs the validation
    """
    _registered_classifiers.add(
        _classifier(basetype=model, to_class=classifier))


def classifier(model):
    """ Decorator version of register, see register(model, classifier) """
    def wrapper(func):
        register(model, func)
    return wrapper


def declassify(model, data):
    """
    !! NOT YET IMPLEMENTED !!

    Declassifies the given *data* from the *model* model/type, any type issue
    will raise TypeError, if no error is raised it will return a python type
    appropriate for the model/class given

    **Keyword arguments**:

    * model -- a model (class) to declassify the data from
    * data -- a python instance
    """
    pass
