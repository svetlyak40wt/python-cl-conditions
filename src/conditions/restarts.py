# coding: utf-8

import threading
from contextlib import contextmanager
from collections import deque

from .exceptions import (
    RestartNotFoundError,
    InvokeRestart)


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
