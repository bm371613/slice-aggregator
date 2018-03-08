from slice_aggregator import heap


def test_indexed_unique_max_heap():
    h = heap.IndexedUniqueMaxHeap()
    h.add(10)
    h.add(20)
    h.add(30)
    h.add(15)
    h.add(20)
    h.add(25)

    assert len(h) == 5
    assert 5 not in h
    assert 10 in h
    assert 15 in h
    assert 20 in h
    assert 25 in h
    assert 30 in h
    assert h.max() == 30

    h.remove(25)
    h.remove(30)
    h.remove(35)

    assert len(h) == 3
    assert 10 in h
    assert 15 in h
    assert 20 in h
    assert 25 not in h
    assert 30 not in h
    assert h.max() == 20
