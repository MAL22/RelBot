import functools
from timeit import default_timer as timer
from datetime import timedelta


def measure_exec_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        print(f'{func.__name__} exec time: {timedelta(seconds=end - start)}')
        return result

    return wrapper
