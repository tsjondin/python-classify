
from classify import classify, intersection


def test_intersection():
    class A:
        a = int

    class B:
        b = str
    i_type = intersection(A, B)
    classify(i_type, {'a': 1, 'b': 'foobar'})
