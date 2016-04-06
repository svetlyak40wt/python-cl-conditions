# coding: utf-8

import threading
from collections import deque

from .exceptions import (
    RestartNotFoundError,
    InvokeRestart)
from .signals import signal


_restarts = threading.local()
_restarts.stack = deque()


def find_restart(name):
    for restart_name, callback in _restarts.stack:
        if restart_name == name:
            return callback


def invoke_restart(name, *args, **kwargs):
    callback = find_restart(name)
    if callback is None:
        raise RestartNotFoundError(name)
    raise InvokeRestart(callback, *args, **kwargs)


class restarts(object):
    def __init__(self, *callbacks):
        self.callbacks = callbacks

    def __enter__(self):
        for callback in self.callbacks:
            name = callback.__name__
            if name == '<lambda>':
                raise RuntimeError('Restart function should have name')
            _restarts.stack.appendleft((name, callback))
        return self

    def __call__(self, callback, *args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            try:
                return signal(e)
            except InvokeRestart as e:
                return e.callback()

    def __exit__(self, *args):
        for i in range(len(self.callbacks)):
            _restarts.stack.popleft()


def restart(callback):
    return restarts(callback)
