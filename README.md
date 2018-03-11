# slice-aggregator

[![Build Status](https://travis-ci.org/bm371613/slice-aggregator.svg?branch=master)](https://travis-ci.org/bm371613/slice-aggregator)

A library for aggregating values assigned to indices by slices

```pydocstring
>>> import slice_aggregator
>>> a = slice_aggregator.ixs_by_slice()
>>> a[-4] += 10
>>> a[13] -= 20
>>> a[-8:]
-10
```

and the other way around

```pydocstring
>>> import slice_aggregator
>>> a = slice_aggregator.slices_by_ix()
>>> a[:-4] += 10
>>> a[-10:13] -= 20
>>> a[-8]
-10
```
