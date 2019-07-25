"""
author songjie
"""
from contextlib import contextmanager

from .function import debug


def default_callback(**kwargs):
    """
    HelperContext default callback
    :return:
    """
    pass


class HelperContext(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @contextmanager
    def auto_handle_exception(self,
                              before_callback=default_callback,
                              error_callback=default_callback,
                              after_callback=default_callback,
                              throw_exception_flag=False,
                              **kwargs
                              ):
        try:
            before_callback(**kwargs)
            yield
            after_callback(**kwargs)
        except Exception as e:
            error_callback(**kwargs)
            if throw_exception_flag:
                debug(e)
