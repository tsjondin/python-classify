
from classify import classify
from pytest import raises


def test_class_returns_instanceof_type():
    class A:
        a = str
        b = int
        c = float
    assert isinstance(classify({
        'a': 'Hello world!',
        'b': 1,
        'c': 1.1
    }, A), A)


def test_class_any_failure_throws():
    class A:
        a = str
        b = int
        c = float
    with raises(TypeError):
        classify({
            'a': 'Hello world!',
            'b': 1.1,
            'c': 1.1
        }, A)


def test_class_may_be_nested():
    class B:
        c = str
    class A:
        b = B
    d = classify({
        'b': {
            'c': 'Hello world!'
        },
    }, A)
    assert isinstance(d, A)
    assert isinstance(d.b, B)


def test_class_any_failure_in_nesting_throws():
    class B:
        d = int
    class A:
        a = str
        b = B
        c = float
    with raises(TypeError):
        classify({
            'a': 'Hello world!',
            'b': {
                'd': 1.1
            },
            'c': 1.1
        }, A)
