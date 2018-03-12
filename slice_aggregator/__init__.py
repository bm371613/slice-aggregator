from . import (
    __about__ as about,
    by_ixs,
    by_slices,
)

V = by_slices.V
ZF = by_slices.ZF
ZT = by_slices.ZT


def ixs_by_slices(*, zero_factory: ZF = None, zero_test: ZT = None) -> by_slices.Aggregator[V]:
    """ Returns an object that allows assigning values to indices and aggregating them by slices

    Example:

    >>> a = ixs_by_slices()
    >>> a[-4] += 10
    >>> a[13] -= 20
    >>> a[-8:]
    -10

    :param zero_factory: callable returning additive identity (default returns 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating index-assigned values by slices
    """
    return by_slices.UnboundedAggregator(
        negative=by_slices.VariableSizeLeftBoundedAggregator(zero_factory=zero_factory,
                                                             zero_test=zero_test),
        nonnegative=by_slices.VariableSizeLeftBoundedAggregator(zero_factory=zero_factory,
                                                                zero_test=zero_test),
    )


def slices_by_ixs(*, zero_factory: ZF = None, zero_test: ZT = None) -> by_ixs.Aggregator[V]:
    """ Returns an object that allows assigning values to slices and aggregating them by indices

    Example:

    >>> a = slices_by_ixs()
    >>> a[:-4] += 10
    >>> a[-10:13] -= 20
    >>> a[-8]
    -10

    :param zero_factory: callable returning additive identity (default returns 0)
    :param zero_test: test for zero equality (default compares to `zero` parameter with `==`)
    :return: a new object for aggregating slice-assigned values by indices
    """
    return by_ixs.Aggregator(
        dual=ixs_by_slices(zero_factory=zero_factory, zero_test=zero_test),
        zero_factory=zero_factory,
    )
