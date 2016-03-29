# coding: utf-8

from .handlers import find_handler


def signal(obj):
    callback = find_handler(obj.__class__)
    if callback is None:
        raise obj
    else:
        return callback(obj)
