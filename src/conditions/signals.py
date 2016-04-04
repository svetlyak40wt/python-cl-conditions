# coding: utf-8

from .handlers import find_handler


def signal(e):
    callback = find_handler(e)
    if callback is None:
        raise e
    else:
        return callback(e)
