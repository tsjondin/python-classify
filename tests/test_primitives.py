
from classify import classify
from pytest import raises, mark


def test_int():
    int_type = int
    assert classify(1, int_type) == 1


@mark.parametrize('data', [
    (1.0),
    ("String"),
    (True),
    (False),
    ([]),
    ({})
])
def test_not_int(data):
    int_type = int
    with raises(TypeError):
        classify(data, int_type)


def test_float():
    float_type = float
    assert classify(1.0, float_type) == 1.0


@mark.parametrize('data', [
    (1),
    ("String"),
    (True),
    (False),
    ([]),
    ({})
])
def test_not_float(data):
    float_type = float
    with raises(TypeError):
        classify(data, float_type)


def test_str():
    str_type = str
    assert classify("Hej", str_type) == "Hej"


@mark.parametrize('data', [
    (1),
    (1.0),
    (True),
    (False),
    ([]),
    ({})
])
def test_not_str(data):
    str_type = str
    with raises(TypeError):
        classify(data, str_type)


def test_bool():
    bool_type = bool
    assert classify(True, bool_type) is True


@mark.parametrize('data', [
    (1),
    (1.0),
    (""),
    ([]),
    ({})
])
def test_not_bool(data):
    bool_type = bool
    with raises(TypeError):
        classify(data, bool_type)


def test_none():
    none_type = None
    assert classify(None, none_type) is None


@mark.parametrize('data', [
    (1),
    (1.0),
    (""),
    (True),
    (False),
    ([]),
    ({})
])
def test_not_none(data):
    none_type = None
    with raises(TypeError):
        classify(data, none_type)
