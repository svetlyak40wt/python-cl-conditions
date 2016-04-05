#!/usr/bin/env python

"""
This code is a full reimplementation of the log parser
from "Beyond Exception Handling: Conditions and Restarts"
chapter of the book:

http://www.gigamonkeys.com/book/beyond-exception-handling-conditions-and-restarts.html
"""

import os

from conditions import (
    signal,
    restarts,
    invoke_restart,
    handle)


class MalformedLogEntryError(RuntimeError):
    def __init__(self, text):
        self.text = text
        super(MalformedLogEntryError, self).__init__('Malformed entry')


class LogEntry(object):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return u'LogEntry: {0}'.format(self.text)


class MalformedLogEntry(object):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return u'MalformedEntry: {0}'.format(self.text)


def well_formed_log_entry_p(text):
    return any(text.startswith(level)
               for level in ('ERROR: ',
                             'INFO: ',
                             'DEBUG: '))


def parse_log_file(filename):
    with open(filename) as f:
        return map(parse_log_entry, f.readlines())


def analyze_log(filename):
    for entry in parse_log_file(filename):
        analyze_entry(entry)


def analyze_entry(entry):
    print(entry)


def find_all_logs(path):
    return (os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith('.log'))


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


if __name__ == '__main__':
    current_dir = os.path.dirname(__file__) or '.'
    log_analyzer(current_dir)
