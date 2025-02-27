import functools
import time

def before(advice):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            advice(func, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def after(advice):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            advice(func, result, *args, **kwargs)
            return result
        return wrapper
    return decorator

def around(advice):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return advice(func, *args, **kwargs)
        return wrapper
    return decorator

def on_exception(advice):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                advice(func, e, *args, **kwargs)
                raise e
        return wrapper
    return decorator