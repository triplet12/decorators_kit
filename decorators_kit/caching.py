import functools
import time


def memoize(func):
    '''Кеширование значений функции'''
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



def timed_cache(ttl:int=60, clock=time.monotonic):
    '''Кеширование результатов функции на ttl секунд'''
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