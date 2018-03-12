import collections
import typing

from .by_slices import (
    Aggregator as Dual,
    V,
    ZF,
)

_ASSIGNED_GUARD = object()


class _InplaceAddHelper(collections.namedtuple("_InplaceAddHelper", "callback")):

    def __iadd__(self, value: V) -> typing.Any:
        return self.callback(value)

    def __isub__(self, value: V) -> typing.Any:
        return self.callback(-value)


class Aggregator(typing.Generic[V]):

    def __init__(self, *, dual: Dual, zero_factory: ZF = None):
        self.dual = dual
        self.value_offset = 0 if zero_factory is None else zero_factory()

    def get(self, ix: int) -> V:
        return self.dual[ix:] + self.value_offset

    def inc(self, start: typing.Optional[int], stop: typing.Optional[int], value: V) -> None:
        if start is None:
            if stop is None:
                self.value_offset += value
            else:
                self.dual[stop - 1] += value
        elif stop is None:
            self.dual[start - 1] -= value
            self.value_offset += value
        elif start < stop:
            self.dual[start - 1] -= value
            self.dual[stop - 1] += value
        elif start > stop:
            raise ValueError("start > stop")

    def dec(self, start: typing.Optional[int], stop: typing.Optional[int], value: V) -> None:
        self.inc(start, stop, -value)

    def _inplace_add_callback(self, start: typing.Optional[int], stop: typing.Optional[int],
                              value: V) -> typing.Any:
        self.inc(start, stop, value)
        return _ASSIGNED_GUARD

    def __getitem__(self, item: typing.Union[int, slice]) -> typing.Union[V, _InplaceAddHelper]:
        if isinstance(item, slice):
            if item.step is not None:
                raise ValueError("Slicing with step is not supported")
            return _InplaceAddHelper(lambda v: self._inplace_add_callback(item.start, item.stop, v))
        else:
            return self.get(item)

    def __setitem__(self, key: slice, value: typing.Any) -> None:
        if value is not _ASSIGNED_GUARD:
            raise NotImplementedError("Operation not supported!")
