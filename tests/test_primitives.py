
from classify import classify
from pytest import raises, mark


def test_int():
    int_type = int
    assert classify(int_type, 1) == 1


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
        classify(int_type, data)


def test_float():
    float_type = float
    assert classify(float_type, 1.0) == 1.0


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
        classify(float_type, data)


def test_str():
    str_type = str
    assert classify(str_type, "Hej") == "Hej"


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
        classify(str_type, data)


def test_bool():
    bool_type = bool
    assert classify(bool_type, True) is True


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
        classify(bool_type, data)


def test_none():
    none_type = None
    assert classify(none_type, None) is None


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
        classify(none_type, data)
