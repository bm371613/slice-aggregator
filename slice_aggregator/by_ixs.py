import collections
import typing

from .by_slices import (
    Aggregator as Dual,
    V,
)

_ASSIGNED_GUARD = object()


class _InplaceAddHelper(collections.namedtuple("_AssignableSlice", "callback")):

    def __iadd__(self, value: V) -> typing.Any:
        return self.callback(value)

    def __isub__(self, value: V) -> typing.Any:
        return self.callback(-value)


class Aggregator(typing.Generic[V]):

    def __init__(self, *, dual: Dual, zero: V = 0):
        self.dual = dual
        self.value_offset = zero

    def _increment(self, start: int, stop: int, value: V) -> typing.Any:
        if start is None:
            if stop is None:
                self.value_offset += value
            else:
                self.dual[stop - 1] += value
        elif stop is None:
            self.dual[start - 1] -= value
            self.value_offset += value
        else:
            self.dual[start - 1] -= value
            self.dual[stop - 1] += value
        return _ASSIGNED_GUARD

    def __getitem__(self, item: typing.Union[int, slice]) -> typing.Union[V, _InplaceAddHelper]:
        if isinstance(item, slice):
            if item.step is not None:
                raise ValueError("Slicing with step is not supported")
            if item.start is not None and item.stop is not None and item.start > item.stop:
                raise ValueError("Slicing with start > stop are not supported")
            return _InplaceAddHelper(lambda v: self._increment(item.start, item.stop, v))
        elif isinstance(item, int):
            return self.dual[item:] + self.value_offset
        else:
            raise TypeError("Type not supported", type(item))

    def __setitem__(self, key, value):
        if value is not _ASSIGNED_GUARD:
            raise NotImplementedError("Operation not supported!")
