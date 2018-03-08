import typing

from .heap import IndexedUniqueMaxHeap


def binary_tail(n: int) -> int:
    """ The last 1 digit and the following 0s of a binary representation, as a number """
    return ((n ^ (n - 1)) + 1) >> 1


V = typing.TypeVar('V')  # value type
T = typing.Union[typing.MutableSequence[V], typing.MutableMapping[int, V]]  # table type


class Aggregator(typing.Generic[V]):

    def __getitem__(self, item: typing.Union[int, slice]) -> V:
        raise NotImplementedError()

    def __setitem__(self, ix: int, value: V) -> None:
        raise NotImplementedError()


class LeftBoundedAggregator(Aggregator):

    def __init__(self, table: T, zero: V):
        self.table = table
        self.zero = zero

    def _nonzero_ix_upper_bound(self) -> int:
        raise NotImplementedError()

    def __getitem__(self, item: typing.Union[int, slice]) -> V:
        if isinstance(item, slice):
            if item.step is not None:
                raise ValueError("Slicing with step is not supported")
            start = item.start
            stop = item.stop
        elif isinstance(item, int):
            if item < 0:
                raise IndexError("Index out of range")
            start = item
            stop = item + 1
        else:
            raise TypeError("Type not supported", type(item))

        bound = self._nonzero_ix_upper_bound()
        if start is None:
            start = 0
        if stop is None:
            stop = bound + 1
        result = self.zero
        while start != stop and (start <= bound or stop <= bound):
            if start < stop:
                result += self.table[start]
                start += binary_tail(start + 1)  # +1 for 0-based indexing
            else:
                result -= self.table[stop]
                stop += binary_tail(stop + 1)  # +1 for 0-based indexing
        return result

    def __setitem__(self, ix: int, value: V) -> None:
        if not isinstance(ix, int):
            raise TypeError("Type not supported", type(ix))
        if ix < 0:
            raise IndexError("Index out of range")

        diff = value - self[ix]
        while ix >= 0:
            self.table[ix] += diff
            ix -= binary_tail(ix + 1)  # +1 for 0-based indexing


class FixedSizeAggregator(LeftBoundedAggregator):

    def __init__(self, table: typing.MutableSequence[V], zero: V):
        super().__init__(table, zero)

    def _nonzero_ix_upper_bound(self):
        return len(self.table) - 1


class VariableSizeLeftBoundedAggregator(LeftBoundedAggregator):

    class Table(typing.MutableMapping[int, V]):

        def __init__(self, zero):
            super().__init__()
            self.zero = zero
            self.data = {}

        def __getitem__(self, ix):
            return self.data.get(ix, self.zero)

        def __setitem__(self, ix, value):
            if value == self.zero:
                del self.data[ix]
            else:
                self.data[ix] = value

        def __delitem__(self, ix):
            del self.data

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

    def __init__(self, zero):
        super().__init__(self.Table(zero), zero)
        self.heap = IndexedUniqueMaxHeap()

    def _nonzero_ix_upper_bound(self) -> int:
        if not self.table.data:
            return 0
        return self.heap.max()

    def __setitem__(self, ix: int, value: V) -> None:
        super().__setitem__(ix, value)
        if value == self.zero:
            self.heap.remove(ix)
        else:
            self.heap.add(ix)


class UnboundedAggregator(Aggregator):

    def __init__(self, negative: LeftBoundedAggregator, nonnegative: LeftBoundedAggregator):
        self.negative = negative
        self.nonnegative = nonnegative

    def __getitem__(self, item: typing.Union[int, slice]) -> V:
        if isinstance(item, slice):
            if item.step is not None:
                raise ValueError("Slicing with step is not supported")
            if item.start is None:
                if item.stop is None:
                    return self.negative[:] + self.nonnegative[:]
                elif item.stop > 0:
                    return self.negative[:] + self.nonnegative[:item.stop]
                else:
                    return self.negative[-item.stop:]
            elif item.stop is None:
                if item.start >= 0:
                    return self.nonnegative[item.start:]
                else:
                    return self.negative[:-item.start] + self.nonnegative[:]
            elif item.start >= item.stop:
                return self.nonnegative.zero
            elif 0 <= item.start:
                return self.nonnegative[item.start:item.stop]
            elif item.stop <= 0:
                return self.negative[-item.stop:-item.start]
            else:
                return self.negative[:-item.start] + self.nonnegative[:item.stop]
        elif isinstance(item, int):
            if item < 0:
                return self.negative[-1 - item]
            else:
                return self.nonnegative[item]
        else:
            raise TypeError("Type not supported", type(item))

    def __setitem__(self, ix: int, value: V) -> None:
        if ix < 0:
            self.negative[-1 - ix] = value
        else:
            self.nonnegative[ix] = value


def fixed_size(size: int, zero: V = 0) -> Aggregator:
    return FixedSizeAggregator([zero for _ in range(size)], zero)


def flexible(zero: V = 0) -> Aggregator:
    return UnboundedAggregator(
        VariableSizeLeftBoundedAggregator(zero),
        VariableSizeLeftBoundedAggregator(zero),
    )
