Underlying data structure
=========================

by_slice
--------

The core concept is a data structure similar to a
`Fenwick tree <https://en.wikipedia.org/wiki/Fenwick_tree>`_ that allows assigning values
to nonnegative indices and efficiently computing suffix sums.
Where a Fenwick tree would store an aggregate for `[a, b]`, it stores an aggregate for
`[b, b + b - a]`.
With that change, while modifying the value for index `ix` it goes along decreasing indices, so it
doesn't need to know the size of the internal table (maximum allowed value).
So all values above the biggest index modified by the user are zeroes.
That's useful for computing suffix sums - moving along increasing indices, the biggest one the user
has set to a non-zero value is where one can stop.
A max heap with an index is used to efficiently track these upper bounds.

The unbounded variant is just a combination of two such left-bounded data structures.

by_ix
-----

This a thin layer on top of the previous data structure.
Incrementing `[a, b)` translates to decrementing `a - 1` and incrementing `b - 1` of the underlying
`by_slice` aggregator, and aggregating slices translates to a suffix sum.
