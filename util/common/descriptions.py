import time
import traceback
from functools import wraps


def run_time(func):
    @wraps(func)
    def wrapper():
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        print("used time:{}s".format(end - start))

    return wrapper


def bool_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    return wrapper
