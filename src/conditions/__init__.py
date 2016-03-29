__version__ = "0.1.0"

import threading
from contextlib import contextmanager
from collections import deque


_handlers = threading.local()
_handlers.stack = deque()

_restarts = threading.local()
_restarts.stack = deque()


class InvokeRestart(Exception):
    def __init__(self, callback, *args, **kwargs):
        """This exception helps to unwind stack and to call
        given callback on the frame where it was bound.
        """
        self.callback = callback
        self.args = args
        self.kwargs = kwargs


class RestartNotFoundError(RuntimeError):
    pass


def find_callback(cls):
    for handled_cls, callback in _handlers.stack:
        if handled_cls == cls:
            return callback


def find_restart(name):
    for restart_name, callback in _restarts.stack:
        if restart_name == name:
            return callback


def invoke_restart(name, *args, **kwargs):
    callback = find_restart(name)
    if callback is None:
        raise RestartNotFoundError(name)
    raise InvokeRestart(callback, *args, **kwargs)


@contextmanager
def handle(cls, callback):
    _handlers.stack.appendleft((cls, callback))

    try:
        yield
    finally:
        _handlers.stack.popleft()


@contextmanager
def restart(name, callback):
    _restarts.stack.appendleft((name, callback))

    try:
        yield
    except InvokeRestart as e:
        if e.callback is callback:
            callback(*e.args, **e.kwargs)
        else:
            raise
    finally:
        _restarts.stack.popleft()


def signal(obj):
    callback = find_callback(obj.__class__)
    if callback is None:
        raise obj
    else:
        return callback(obj)
