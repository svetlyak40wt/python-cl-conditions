import threading

from contextlib import contextmanager
from collections import deque


_handlers = threading.local()
_handlers.stack = deque()


@contextmanager
def handle(cls, callback):
    _handlers.stack.appendleft((cls, callback))

    try:
        yield
    finally:
        _handlers.stack.popleft()


def find_handler(e):
    for handled_cls, callback in _handlers.stack:
        if isinstance(e, handled_cls):
            return callback
