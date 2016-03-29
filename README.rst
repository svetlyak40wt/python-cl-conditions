========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-cl-conditions/badge/?style=flat
    :target: https://readthedocs.org/projects/python-cl-conditions
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/svetlyak40wt/python-cl-conditions.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/svetlyak40wt/python-cl-conditions

.. |requires| image:: https://requires.io/github/svetlyak40wt/python-cl-conditions/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/svetlyak40wt/python-cl-conditions/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/svetlyak40wt/python-cl-conditions/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/svetlyak40wt/python-cl-conditions

.. |version| image:: https://img.shields.io/pypi/v/conditions.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/conditions

.. |downloads| image:: https://img.shields.io/pypi/dm/conditions.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/conditions

.. |wheel| image:: https://img.shields.io/pypi/wheel/conditions.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/conditions

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/conditions.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/conditions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/conditions.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/conditions


.. end-badges

Implementation of the Common Lisp's conditions system in Python.

* Free software: BSD license

Installation
============

::

    pip install conditions

Documentation
=============

https://python-cl-conditions.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
