Time and memory complexity
==========================

After assigning values to ``n`` indices/slices that are all within a ``(-v, v)`` interval


+---------------------------+-----------------+
|Reading (aggregating) time |O(log v)         |
+---------------------------+-----------------+
|Writing (assigning) time   |O(log v + log n) |
+---------------------------+-----------------+
|Memory                     |O(n log v)       |
+---------------------------+-----------------+

assuming values and indices are constant-size and basic arithmetic operations on them are constant-time.
