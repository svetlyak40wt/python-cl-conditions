# coding: utf-8

import os
import traceback

from .handlers import find_handler


_activate_debugger = os.environ.get('DEBUG') == 'yes'
if _activate_debugger:
    try:
        from trepan.api import debug
        set_trace = debug
    except ImportError:
        import pdb
        set_trace = pdb.set_trace


def signal(e):
    """
    Some docstrings.
    """
    callback = find_handler(e)
    if callback is None:
        if _activate_debugger:
            print 'Handler for error {0} not found'.format(type(e))
            traceback.print_stack()
            set_trace()
        raise e
    else:
        return callback(e)
