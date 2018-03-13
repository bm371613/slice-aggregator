import typing

from .heap import IndexedUniqueMaxHeap


def binary_tail(n: int) -> int:
    """ The last 1 digit and the following 0s of a binary representation, as a number """
    return ((n ^ (n - 1)) + 1) >> 1


V = typing.TypeVar('V')  # value type
ZF = typing.Callable[[], V]  # zero factory
ZT = typing.Callable[[V], bool]  # zero test


class Aggregator(typing.Generic[V]):
    """ A data structure for assigning values to indices and aggregating them by slices

    It provides a method-based interface and an alternative based on `__getitem__` and slices.

    **Warning**
    Only the method-based interface is suitable for custom values handling inplace operators.
    Read the documentation on advances usage for more details.
    """

    def get(self, start: typing.Optional[int], stop: typing.Optional[int]) -> V:
        """ Get the aggregated value of all indices contained by the specified slice """
        raise NotImplementedError()

    def inc(self, ix: int, value: V) -> None:
        """ Increment the value assigned to an index """
        raise NotImplementedError()

    def dec(self, ix: int, value: V) -> None:
        """ Decrement the value assigned to an index """
        self.inc(ix, -value)

    def set(self, ix: int, value: V) -> None:
        """ Set the value assigned to an index """
        self.inc(ix, value - self.get(ix, ix + 1))

    def __getitem__(self, item: typing.Union[int, slice]) -> V:
        if isinstance(item, slice):
            if item.step is not None:
                raise ValueError("Slicing with step is not supported")
            return self.get(item.start, item.stop)
        else:
            return self.get(item, item + 1)

    def __setitem__(self, ix: int, value: V) -> None:
        self.set(ix, value)


class LeftBoundedAggregator(Aggregator):

    def __init__(self, *, zero_factory: ZF = None):
        if zero_factory is None:
            def zero_factory():
                return 0
        self.zero_factory = zero_factory

    def _table_get(self, ix: int) -> V:
        raise NotImplementedError()

    def _table_set(self, ix: int, value: V) -> None:
        raise NotImplementedError()

    def _nonzero_ix_upper_bound(self) -> int:
        raise NotImplementedError()

    def get(self, start: typing.Optional[int], stop: typing.Optional[int]) -> V:
        if start is not None and start < 0:
            raise IndexError("start is out of range")
        if stop is not None and stop < 0:
            raise IndexError("stop is out of range")
        result = self.zero_factory()
        if start is not None and stop is not None and start >= stop:
            return result
        bound = self._nonzero_ix_upper_bound()
        if start is None:
            start = 0
        if stop is None:
            stop = bound + 1
        while start != stop and (start <= bound or stop <= bound):
            if start < stop:
                result += self._table_get(start)
                start += binary_tail(start + 1)  # +1 for 0-based indexing
            else:
                result -= self._table_get(stop)
                stop += binary_tail(stop + 1)  # +1 for 0-based indexing
        return result

    def inc(self, ix: int, value: V) -> None:
        if ix < 0:
            raise IndexError("ix out of range")
        while ix >= 0:
            self._table_set(ix, self._table_get(ix) + value)
            ix -= binary_tail(ix + 1)  # +1 for 0-based indexing


class FixedSizeAggregator(LeftBoundedAggregator):

    def __init__(self, *, table: typing.MutableSequence[V], zero_factory: ZF = None):
        super().__init__(zero_factory=zero_factory)
        self.table = table

    def _table_get(self, ix: int) -> V:
        return self.table[ix]

    def _table_set(self, ix: int, value: V) -> None:
        self.table[ix] = value

    def _nonzero_ix_upper_bound(self) -> int:
        return len(self.table) - 1


class VariableSizeLeftBoundedAggregator(LeftBoundedAggregator):

    def __init__(self, *, zero_factory: ZF = None, zero_test: ZT = None):
        super().__init__(zero_factory=zero_factory)
        self.table = {}
        self.heap = IndexedUniqueMaxHeap()
        self.zero = zero_factory() if zero_factory is not None else 0  # read only
        if zero_test is None:
            def zero_test(v):
                return v == self.zero
        self.zero_test = zero_test

    def _table_get(self, ix: int) -> V:
        return self.table[ix] if ix in self.table else self.zero

    def _table_set(self, ix: int, value: V) -> None:
        if self.zero_test(value):
            del self.table[ix]
        else:
            self.table[ix] = value

    def _nonzero_ix_upper_bound(self) -> int:
        if not len(self.table):
            return 0
        return self.heap.max()

    def inc(self, ix: int, value: V) -> None:
        new_value = self.get(ix, ix + 1) + value
        super().inc(ix, value)
        if self.zero_test(new_value):
            self.heap.remove(ix)
        else:
            self.heap.add(ix)


class UnboundedAggregator(Aggregator):

    def __init__(self, *, negative: LeftBoundedAggregator, nonnegative: LeftBoundedAggregator):
        self.negative = negative
        self.nonnegative = nonnegative

    def get(self, start: typing.Optional[int], stop: typing.Optional[int]) -> V:
        if start is None:
            if stop is None:
                return self.negative.get(None, None) + self.nonnegative.get(None, None)
            elif stop > 0:
                return self.negative.get(None, None) + self.nonnegative.get(None, stop)
            else:
                return self.negative.get(-stop, None)
        elif stop is None:
            if start >= 0:
                return self.nonnegative.get(start, None)
            else:
                return self.negative.get(None, -start) + self.nonnegative.get(None, None)
        elif start >= stop:
            return self.nonnegative.zero
        elif 0 <= start:
            return self.nonnegative.get(start, stop)
        elif stop <= 0:
            return self.negative.get(-stop, -start)
        else:
            return self.negative.get(None, -start) + self.nonnegative.get(None, stop)

    def inc(self, ix: int, value: V) -> None:
        if ix < 0:
            self.negative.inc(-1 - ix, value)
        else:
            self.nonnegative.inc(ix, value)
