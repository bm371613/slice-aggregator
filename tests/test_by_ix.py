import pytest

from slice_aggregator import ixs_by_slice
from slice_aggregator.by_ix import Aggregator


def test_mixed_slice_types():
    a = Aggregator(dual=ixs_by_slice())
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
    a = Aggregator(dual=ixs_by_slice())
    with pytest.raises(NotImplementedError):
        a[1] = 3
