# slice-aggregator

[![Build Status](https://travis-ci.org/bm371613/slice-aggregator.svg?branch=master)](https://travis-ci.org/bm371613/slice-aggregator)
[![Documentation Status](https://readthedocs.org/projects/slice-aggregator/badge/?version=latest)](http://slice-aggregator.readthedocs.io/en/latest/?badge=latest)

A library for aggregating values assigned to indices by slices

```pydocstring
>>> import slice_aggregator
>>> a = slice_aggregator.ixs_by_slices()
>>> a[-5] += 1
>>> a[10] -= 2.5
>>> a[-10:]
-1.5

```

and the other way around

```pydocstring
>>> import slice_aggregator
>>> a = slice_aggregator.slices_by_ixs()
>>> a[:-5] += 1
>>> a[-10:10] -= 2.5
>>> a[-10]
-1.5

```

[Read the docs](https://slice-aggregator.readthedocs.io/) to find out more!
