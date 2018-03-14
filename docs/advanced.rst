Advanced usage
==============

The library "just works" with value types that:

1. implement addition-like binary operation via Python magic-methods
   (``__add__``, ``__sub__``, ``__sub__``, ``__pos__``)
2. use ``0`` as the neutral element for their addition implementation
3. implement ``__eq__`` that allows testing for equality to zero
4. do not implement inplace addition/subtraction (``__iadd__``, ``__isub__``)

All Python's numeric types (``int``, ``float``, ``long``, ``complex``) fall into that category.

The first condition is a hard requirement for any type to be used for values,
but the others are not.
You can use another value as a neutral element by using the ``zero_factory`` parameter,
you don't have to worry about ``__eq__`` if you supply ``zero_test``
and you can have ``__iadd__`` and ``__isub__`` if you use the method-based interface.

Example:

    >>> import numpy as np
    >>>
    >>> def zero_factory():
    ...     return np.zeros(3)
    >>>
    >>> zero = zero_factory()
    >>>
    >>> def zero_test(v):
    ...     return np.array_equal(v, zero)
    >>>
    >>> import slice_aggregator
    >>>
    >>> a = slice_aggregator.ixs_by_slices(zero_factory=zero_factory, zero_test=zero_test)
    >>> a.inc(-5, np.array([1, 0, 3.5]))
    >>> a.dec(10, np.array([2.5, -1, 0]))
    >>> tuple(a.get(-10, None))  # a[-10:]
    (-1.5, 1.0, 3.5)
