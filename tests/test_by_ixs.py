import numpy as np
import pytest

from slice_aggregator import ixs_by_slices
from slice_aggregator.by_ixs import Aggregator


def test_mixed_slice_types():
    a = Aggregator(dual=ixs_by_slices())
    a[:] += 1
    a[-10:] += 100
    a[-5:5] -= 200
    a[:10] += 10

    assert a[-11] == 11
    assert a[-10] == 111
    assert a[-6] == 111
    assert a[-5] == -89
    assert a[4] == -89
    assert a[5] == 111
    assert a[9] == 111
    assert a[10] == 101


def test_setitem_error():
    a = Aggregator(dual=ixs_by_slices())
    with pytest.raises(NotImplementedError):
        a[1] = 3


def test_numpy_array():
    def zero_factory():
        return np.zeros(4)

    zero = zero_factory()

    def zero_test(v):
        return np.array_equal(zero, v)

    a = Aggregator(
        dual=ixs_by_slices(zero_factory=zero_factory, zero_test=zero_test),
        zero_factory=zero_factory,
    )
    a.inc(None, None, np.array((1, 0, 0, 0)))
    a.inc(-10, None, np.array((0, 1, 0, 0)))
    a.dec(-5, 5, np.array((0, 0, 1, 0)))
    a.inc(None, 10, np.array((0, 0, 0, 1)))

    assert np.array_equal(a.get(-11), np.array((1, 0, 0, 1)))
    assert np.array_equal(a.get(-10), np.array((1, 1, 0, 1)))
    assert np.array_equal(a.get(-6), np.array((1, 1, 0, 1)))
    assert np.array_equal(a.get(-5), np.array((1, 1, -1, 1)))
    assert np.array_equal(a.get(4), np.array((1, 1, -1, 1)))
    assert np.array_equal(a.get(5), np.array((1, 1, 0, 1)))
    assert np.array_equal(a.get(9), np.array((1, 1, 0, 1)))
    assert np.array_equal(a.get(10), np.array((1, 1, 0, 0)))
