import functools
import time


def memoize(func):
    cache: dict = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache.keys():
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper


def retry(times: int, exceptions: tuple) :
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times - 1):

                try:
                    return func(*args, **kwargs)
                except exceptions:
                    pass

            return func(*args, **kwargs)
        return wrapper
    return decorator



def timed_cache(ttl:int=60, clock=time.monotonic):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = clock()
            if args in cache:
                result, expires_at = cache[args]
                if expires_at <= now:
                    del cache[args]
                else:
                    return result
            result = func(*args)
            cache[args] = result, now + ttl
            return result
        return wrapper
    return decorator


