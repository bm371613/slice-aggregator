.. slice-aggregator documentation master file, created by
   sphinx-quickstart on Mon Mar 12 21:58:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to slice-aggregator's documentation!
============================================

It is a library for aggregating values assigned to indices by slices

    >>> import slice_aggregator
    >>> a = slice_aggregator.ixs_by_slices()
    >>> a[-4] += 10
    >>> a[13] -= 20
    >>> a[-8:]
    -10

and the other way around

    >>> import slice_aggregator
    >>> a = slice_aggregator.slices_by_ixs()
    >>> a[:-4] += 10
    >>> a[-10:13] -= 20
    >>> a[-8]
    -10

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api.rst
   advanced.rst
   complexity.rst
   implementation.rst


Indices and tables
==================

* :ref:`genindex`
