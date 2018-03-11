from . import (
    by_ix,
    by_slice,
)

V = by_slice.V
Z = by_slice.Z


def ixs_by_slice(*, zero: V = 0, zero_test: Z = None) -> by_slice.Aggregator[V]:
    """ Returns an object that allows assigning values to indices and aggregating them by slices

    Example:

    >>> a = ixs_by_slice()
    >>> a[-4] += 10
    >>> a[13] -= 20
    >>> a[-8:]
    -10

    :param zero: additive identity (default 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating index-assigned values by slices
    """
    return by_slice.UnboundedAggregator(
        negative=by_slice.VariableSizeLeftBoundedAggregator(zero=zero, zero_test=zero_test),
        nonnegative=by_slice.VariableSizeLeftBoundedAggregator(zero=zero, zero_test=zero_test),
    )


def slices_by_ix(*, zero: V = 0, zero_test: Z = None) -> by_ix.Aggregator[V]:
    """ Returns an object that allows assigning values to slices and aggregating them by indices

    Example:

    >>> a = slices_by_ix()
    >>> a[:-4] += 10
    >>> a[-10:13] -= 20
    >>> a[-8]
    -10

    :param zero: additive identity (default 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating slice-assigned values by indices
    """
    return by_ix.Aggregator(dual=ixs_by_slice(zero=zero, zero_test=zero_test), zero=zero)
