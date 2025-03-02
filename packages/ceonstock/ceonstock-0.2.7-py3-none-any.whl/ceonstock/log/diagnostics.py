import inspect
from copy import deepcopy


def init_args():
    """Gets the locals() of the caller, returns without the 'self' key"""
    # TODO automatically get locals from caller so that it doesn't have to be passed by the user
    frame = inspect.currentframe()
    caller_locals = deepcopy(frame.f_back.f_locals)
    caller_locals.pop("self")
    return caller_locals
