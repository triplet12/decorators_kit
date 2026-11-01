from decorators_kit import memoize, timed_cache


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def time(self) -> float:
        return self.now


# ---------- memoize ----------

def test_memoize_calls_function_once_for_same_args():
    calls = 0

    @memoize
    def square(x):
        nonlocal calls
        calls += 1
        return x * x

    assert square(4) == 16
    assert square(4) == 16
    assert calls == 1


def test_memoize_caches_different_args_separately():
    calls = 0

    @memoize
    def square(x):
        nonlocal calls
        calls += 1
        return x * x

    square(2)
    square(3)
    square(2)
    assert calls == 2


def test_memoize_caches_falsy_results():
    calls = 0

    @memoize
    def zero(x):
        nonlocal calls
        calls += 1
        return 0

    zero(1)
    zero(1)
    assert calls == 1


# ---------- timed_cache ----------

def make_counted(clock: FakeClock, ttl: int = 60):
    """Функция под timed_cache, которая считает свои вызовы."""
    @timed_cache(ttl=ttl, clock=clock.time)
    def get_value(x):
        get_value.calls += 1
        return x * 10

    get_value.calls = 0
    return get_value


def test_fresh_result_comes_from_cache():
    clock = FakeClock()
    get_value = make_counted(clock)

    assert get_value(1) == 10
    clock.now = 30
    assert get_value(1) == 10
    assert get_value.calls == 1


def test_expired_result_is_recomputed():
    clock = FakeClock()
    get_value = make_counted(clock)

    get_value(1)
    clock.now = 61
    get_value(1)
    assert get_value.calls == 2


def test_result_expires_exactly_at_ttl():
    clock = FakeClock()
    get_value = make_counted(clock)

    get_value(1)
    clock.now = 60
    get_value(1)
    assert get_value.calls == 2


def test_timed_cache_keeps_args_separately():
    clock = FakeClock()
    get_value = make_counted(clock)

    assert get_value(1) == 10
    assert get_value(2) == 20
    assert get_value(1) == 10
    assert get_value.calls == 2


def test_each_function_has_own_cache():
    clock = FakeClock()

    @timed_cache(ttl=60, clock=clock.time)
    def double(x):
        return x * 2

    @timed_cache(ttl=60, clock=clock.time)
    def square(x):
        return x * x

    assert double(5) == 10
    assert square(5) == 25