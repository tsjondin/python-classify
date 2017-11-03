
from classify import classify, union
from pytest import mark


@mark.parametrize('T,data', [
    (union(int, float), 1),
    (union(int, float), 1.0),
])
def test_union(T, data):
    assert classify(T, data) == data
