#!/usr/bin/env python

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


def parse_log_entry(text):
    text = text.strip()

    if well_formed_log_entry_p(text):
        return LogEntry(text)
    else:
        def use_value(obj):
            return obj

        with restarts(use_value,
                      parse_log_entry) as call:
            return call(signal, MalformedLogEntryError(text))

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


def log_analyzer(path):
  with handle(MalformedLogEntryError,
                  lambda (c):
                      invoke_restart('use_value',
                                     MalformedLogEntry(c.text))):
    for filename in find_all_logs(path):
        analyze_log(filename)


if __name__ == '__main__':
    log_analyzer(os.path.dirname(__file__) or '.')
