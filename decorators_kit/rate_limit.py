import functools
import time


def retry(times: int, exceptions: tuple, delay: int=1, backoff:int=2, sleep=time.sleep):
    '''Выполнение функции times раз если падает exceptions'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for _ in range(times - 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    sleep(current_delay)
                    current_delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator