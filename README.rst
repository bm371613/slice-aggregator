slice-aggregator
================

.. image:: https://travis-ci.org/bm371613/slice-aggregator.svg?branch=master
    :target: https://travis-ci.org/bm371613/slice-aggregator
.. image:: https://readthedocs.org/projects/slice-aggregator/badge/?version=latest
    :target: http://slice-aggregator.readthedocs.io/en/latest/?badge=latest

A library for aggregating values assigned to indices by slices

.. code-block:: pycon

    >>> import slice_aggregator
    >>> a = slice_aggregator.ixs_by_slices()
    >>> a[-5] += 1
    >>> a[10] -= 2.5
    >>> a[-10:]
    -1.5

and the other way around

.. code-block:: pycon

    >>> import slice_aggregator
    >>> a = slice_aggregator.slices_by_ixs()
    >>> a[:-5] += 1
    >>> a[-10:10] -= 2.5
    >>> a[-10]
    -1.5

`Read the docs <https://slice-aggregator.readthedocs.io/>`_ to find out more!

Installation
------------

.. code-block:: shell

    pip install slice-aggregator
