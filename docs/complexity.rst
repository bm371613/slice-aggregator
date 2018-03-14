Time and memory complexity
==========================

After assigning values to ``n`` unique indices (we treat a slice as, up to two, indices)
that are all within a ``(-v, v)`` interval:


+---------------------------+-----------------+
|Reading (aggregating) time |O(log v)         |
+---------------------------+-----------------+
|Writing (assigning) time   |O(log v + log n) |
+---------------------------+-----------------+
|Memory                     |O(n log v)       |
+---------------------------+-----------------+

Assumptions:
 - values and indices are constant-size and basic arithmetic operations on them are constant-time
 - set item and get item on a ``dict`` are constant-time (which is true on average)
