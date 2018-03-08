import pytest

from slice_aggregator import by_ix


def test_mixed_slice_types():
    a = by_ix.flexible()
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
    a = by_ix.flexible()
    with pytest.raises(NotImplementedError):
        a[1] = 3
