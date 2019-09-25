========
Overview
========

Implementation of the Common Lisp's conditions system in Python.

Free software: BSD license.

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

Rationale
=========

Common Lisp (CL) has a very rich condition system. Conditions in CL are a kind
of signals, used not only for exception handling but also in some other patterns.
There is a very good explanation of how they work – a chapter from the book
Practical Common Lisp by Peter Seibel:
`Beyond Exception Handling: Conditions and Restarts`_.

Python's exceptions cover only one scenario from this book, but Common Lisp's conditions
allows more interesting usage, particularly "restarts". A restart is a way to continue
code execution after an exception was signaled, without unwinding the call stack.
I'll repeat: without unwinding the call stack.

Moreover, conditions allow the author of the library to define various cases to be
chosen to handle the exception.

.. _`Beyond Exception Handling: Conditions and Restarts`: http://www.gigamonkeys.com/book/beyond-exception-handling-conditions-and-restarts.html

Example
-------

Here is an example from the book, but implemented in Python using the `conditions`_ library::

    def parse_log_entry(text):
        """This function does all real job on log line parsing.
        it setup two cases for restart parsing if a line
        with wrong format was found.

        Restarts:
        - use_value: just retuns an object it was passed. This can
          be any value.
        - reparse: calls `parse_log_entry` again with other text value.
          Beware, this call can lead to infinite recursion.
        """
        text = text.strip()

        if well_formed_log_entry_p(text):
            return LogEntry(text)
        else:
            def use_value(obj):
                return obj
            def reparse(text):
                return parse_log_entry(text)

            with restarts(use_value,
                          reparse) as call:
                return call(signal, MalformedLogEntryError(text))


    def log_analyzer(path):
        """This procedure replaces every line which can't be parsed
        with special object MalformedLogEntry.
        """
        with handle(MalformedLogEntryError,
                      lambda (c):
                          invoke_restart('use_value',
                                         MalformedLogEntry(c.text))):
            for filename in find_all_logs(path):
                analyze_log(filename)


    def log_analyzer2(path):
        """This procedure considers every line which can't be parsed
        as a line with ERROR level.
        """
        with handle(MalformedLogEntryError,
                      lambda (c):
                          invoke_restart('reparse',
                                         'ERROR: ' + c.text)):
            for filename in find_all_logs(path):
                analyze_log(filename)

What we have here is a function ``parse_log_entry``, which defines two ways of
handling an exceptional situation: ``use_value`` and ``reparse``. But the
decision of how bad lines should be handled is made by the high level function
``log_analyser``. The original book chapter has only one version of
``log_analyser``, but I've added an alternative ``log_analyser2`` to illustrate
why restarts are a useful pattern. The value of this pattern is in the ability
to move the decision making code from low level library functions into the
higher level business logic.

The full version of this example can be found in `example/example.py`_.

.. _conditions: https://github.com/svetlyak40wt/python-cl-conditions
.. _`example/example.py`: https://github.com/svetlyak40wt/python-cl-conditions/blob/master/example/example.py

Installation
============

::

    pip install conditions

Documentation
=============

https://python-cl-conditions.readthedocs.org/

Development
===========

To run all tests run::

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


Related projects
================

There is also the withrestart_ Python library, created with
the same intent as conditions_. But it has a clunky API and
a weird name, and seems abandoned since 2010.

.. _withrestart: https://pypi.python.org/pypi/withrestart
