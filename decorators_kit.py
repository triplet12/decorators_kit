import functools


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