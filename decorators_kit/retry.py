import functools
import time


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