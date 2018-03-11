from . import (
    by_ix,
    by_slice,
)

V = by_slice.V


def ixs_by_slice(*, zero: V = 0) -> by_slice.Aggregator[V]:
    """ Returns an object that allows assigning values to indices and aggregating them by slices

    Example:

    >>> a = ixs_by_slice()
    >>> a[-4] += 10
    >>> a[13] -= 20
    >>> a[-8:]
    -10

    :param zero: additive identity (default 0)
    :return: a new object for aggregating index-assigned values by slices
    """
    return by_slice.UnboundedAggregator(
        negative=by_slice.VariableSizeLeftBoundedAggregator(zero=zero),
        nonnegative=by_slice.VariableSizeLeftBoundedAggregator(zero=zero),
    )


def slices_by_ix(*, zero: V = 0) -> by_ix.Aggregator[V]:
    """ Returns an object that allows assigning values to slices and aggregating them by indices

    Example:

    >>> a = slices_by_ix()
    >>> a[:-4] += 10
    >>> a[-10:13] -= 20
    >>> a[-8]
    -10

    :param zero: additive identity (default 0)
    :return: a new object for aggregating slice-assigned values by indices
    """
    return by_ix.Aggregator(dual=ixs_by_slice(zero=zero), zero=zero)
