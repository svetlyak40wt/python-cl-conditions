# coding: utf-8


class InvokeRestart(Exception):
    def __init__(self, callback, *args, **kwargs):
        """This exception helps to unwind stack and to call
        given callback on the frame where it was bound.
        """
        self.callback = lambda: callback(*args, **kwargs)


class RestartNotFoundError(RuntimeError):
    pass
