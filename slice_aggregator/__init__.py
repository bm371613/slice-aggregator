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

    :param zero_factory: callable returning additive identity
    :param zero_test: test for equality to zero
    :return: a new instance of :class:`slice_aggregator.by_slices.Aggregator`
    """
    return by_slices.UnboundedAggregator(
        negative=by_slices.VariableSizeLeftBoundedAggregator(zero_factory=zero_factory,
                                                             zero_test=zero_test),
        nonnegative=by_slices.VariableSizeLeftBoundedAggregator(zero_factory=zero_factory,
                                                                zero_test=zero_test),
    )


def slices_by_ixs(*, zero_factory: ZF = None, zero_test: ZT = None) -> by_ixs.Aggregator[V]:
    """ Returns an object that allows assigning values to slices and aggregating them by indices

    :param zero_factory: callable returning additive identity
    :param zero_test: test for equality to zero
    :return: a new instance of :class:`slice_aggregator.by_ixs.Aggregator`
    """
    return by_ixs.Aggregator(
        dual=ixs_by_slices(zero_factory=zero_factory, zero_test=zero_test),
        zero_factory=zero_factory,
    )
