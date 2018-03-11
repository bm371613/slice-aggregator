import pytest

from slice_aggregator.by_slice import (
    FixedSizeAggregator,
    UnboundedAggregator,
    VariableSizeLeftBoundedAggregator,
    binary_tail,
)


def test_binary_tail():
    assert binary_tail(0b0) == 0b0
    assert binary_tail(0b1) == 0b1
    assert binary_tail(0b1101001) == 0b1
    assert binary_tail(0b1101010) == 0b10
    assert binary_tail(0b1101100) == 0b100
    assert binary_tail(0b1101000) == 0b1000


def test_fixed_size():
    a = FixedSizeAggregator(table=[0] * 10, zero=0)
    a[0] = 1
    a[5] -= 10
    a[9] += 100

    assert a[5] == -10
    assert a[0:5] == 1
    assert a[6:8] == 0
    assert a[4:] == 90
    assert a[:6] == -9
    assert a[:] == 91


def test_fixed_size_index_errors():
    a = FixedSizeAggregator(table=[0] * 10, zero=0)

    with pytest.raises(IndexError):
        a[-1] = 1
    with pytest.raises(IndexError):
        a[10] = 1


def test_custom_values():

    class V:

        def __init__(self, v):
            self.v = v

        def __eq__(self, other):
            return V(self.v == other.v)

        def __add__(self, other):
            return V(self.v * other.v)

        def __sub__(self, other):
            return V(self.v / other.v)

        def __neg__(self):
            return V(-self.v)

    a = FixedSizeAggregator(table=[V(1)] * 10, zero=V(1))
    a[0] = V(4)
    a[3] = V(8)
    a[8] = V(2)

    assert a[2].v == 1
    assert a[3:].v == 16
    assert a[:8].v == 32
    assert a[:].v == 64


def test_variable_size_removes_unnecessary_data():
    a = VariableSizeLeftBoundedAggregator(zero=0)
    a[3] += 10
    a[15] += 15
    assert len(a.table) == 2
    assert len(a.heap) == 2
    a[3] -= 10
    assert len(a.table) == 1
    assert len(a.heap) == 1


def test_unbounded():
    a = UnboundedAggregator(
        negative=VariableSizeLeftBoundedAggregator(zero=0),
        nonnegative=VariableSizeLeftBoundedAggregator(zero=0),
    )
    m = 10 ** 12
    a[-6 * m] = 1
    a[-1 * m] -= 10
    a[8 * m] += 100

    assert a[-1 * m] == -10
    assert a[0:2 * m] == 0
    assert a[-2 * m:] == 90
    assert a[:0] == -9
    assert a[:] == 91
