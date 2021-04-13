import logging
logger = logging.getLogger(__name__)


def log_function_call(f):
    def wrapper(*args, **kwargs):
        print(f.__name__, "args", args, "kwargs", kwargs)
        cr = f(*args, **kwargs)
        print(f.__name__, "result", cr)
        return cr
    return wrapper
