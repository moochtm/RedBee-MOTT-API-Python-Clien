import functools

import logging
logger = logging.getLogger(__name__)


def log_function_call(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        logger.info('-'*60)
        logger.info(f"Calling {f.__name__}({signature})")
        return f(*args, **kwargs)
    return wrapper


@log_function_call
def test(msg):
    print(msg)


if __name__ == '__main__':
    test("bob")