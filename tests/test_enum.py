
from classify import classify
from pytest import raises
from enum import Enum, IntEnum


def test_enum_select_by_name():
    enum_type = Enum('TestEnum', [('A', 1), ('B', 2)])
    assert classify('A', enum_type) is enum_type.A


def test_enum_select_by_non_existing_name():
    enum_type = Enum('TestEnum', [('A', 1), ('B', 2)])
    with raises(TypeError):
        classify('C', enum_type)


def test_intenum_select_by_value():
    enum_type = IntEnum('TestEnum', [('A', 1), ('B', 2)])
    assert classify(1, enum_type) is enum_type.A


def test_intenum_select_by_non_existing_value():
    enum_type = IntEnum('TestEnum', [('A', 1), ('B', 2)])
    with raises(TypeError):
        classify(3, enum_type)
