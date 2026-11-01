import functools
import time
from .exceptions import RateLimitExceeded


def rate_limit(calls=5, period=1, clock=time.monotonic):
    '''Ограничение вызовов функции на period секунд'''
    def decorator(func):
        calls_history = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = clock()

            while calls_history and calls_history[0] <= now - period:
                del calls_history[0]
            if len(calls_history) >= calls:
                raise RateLimitExceeded(f'Не больше {calls} вызовов за {period} с')
            else:
                calls_history.append(now)
                return func(*args, **kwargs)
        return wrapper
    return decorator