""" Modul for decorators.
"""

import time


def one_moment(func):
    """ Waits one second before calling function. """
    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, *kwargs)
    return wrapper


def slow_down(func, sec=1):
    """ Waits a given number of seconds before calling the function."""
    one_moment(func)
    return one_moment


def benchmark(func):
    """ The decorator, deducing the time, which took the execution of the decorated function.
    """

    def wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        res = func(*args, **kwargs)
        run_time = time.perf_counter() - t_start
        print(f"Finiched {func.__name__} in {run_time:.4f}sec")
        return res
    return wrapper


def print_input_argument(func):
    """ Print arguments that are passed to the function. 
    """

    def wrapper(*args, **kwargs):
        print(f'The function "{func.__name__}" has arguments: ', end='\n')
        if args:
            for arg in args:
                print(arg)
        if kwargs:        
            for kwarg in kwargs:
                print(kwarg)
        return func(*args, **kwargs)

    return wrapper


def call_counter(func):
    """ Decorator for count the number of times a function has been called. 
    """

    def helper(*args, **kwargs):
        helper.calls += 1
        print(f'The function "{func.__name__}" was called: {helper.calls}times')
        return func(*args, **kwargs)
    helper.calls = 0
    return helper
