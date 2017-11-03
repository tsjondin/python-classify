from classify.classify import _get_metatype, _classify_instance, classify, classifier, register # flake8: noqa
from classify.union import _Union, classify_union, union # flake8: noqa
from classify.intersection import _Intersection, intersection # flake8: noqa
from classify.typedlist import _TypedList, classify_list, typedlist # flake8: noqa

register(_Union, classify_union)
register(_TypedList, classify_list)
