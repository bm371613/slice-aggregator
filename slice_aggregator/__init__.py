from . import (
    by_ixs,
    by_slices,
)

V = by_slices.V
Z = by_slices.Z


def ixs_by_slices(*, zero: V = 0, zero_test: Z = None) -> by_slices.Aggregator[V]:
    """ Returns an object that allows assigning values to indices and aggregating them by slices

    Example:

    >>> a = ixs_by_slices()
    >>> a[-4] += 10
    >>> a[13] -= 20
    >>> a[-8:]
    -10

    :param zero: additive identity (default 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating index-assigned values by slices
    """
    return by_slices.UnboundedAggregator(
        negative=by_slices.VariableSizeLeftBoundedAggregator(zero=zero, zero_test=zero_test),
        nonnegative=by_slices.VariableSizeLeftBoundedAggregator(zero=zero, zero_test=zero_test),
    )


def slices_by_ixs(*, zero: V = 0, zero_test: Z = None) -> by_ixs.Aggregator[V]:
    """ Returns an object that allows assigning values to slices and aggregating them by indices

    Example:

    >>> a = slices_by_ixs()
    >>> a[:-4] += 10
    >>> a[-10:13] -= 20
    >>> a[-8]
    -10

    :param zero: additive identity (default 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating slice-assigned values by indices
    """
    return by_ixs.Aggregator(dual=ixs_by_slices(zero=zero, zero_test=zero_test), zero=zero)
