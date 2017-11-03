
from classify import classify, intersection


class A:
    a = int


class B:
    b = str


def test_intersection():
    i_type = intersection(A, B)
    classify({'a': 1, 'b': 'foobar'}, i_type)
