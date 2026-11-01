import pytest
from decorators_kit import retry


def no_sleep(seconds: float) -> None:
    """Подмена time.sleep: ничего не ждёт."""


def make_flaky(fail_times: int):
    """Функция, которая падает fail_times раз, а потом возвращает 'ok'."""
    def flaky():
        flaky.calls += 1
        if flaky.calls <= fail_times:
            raise ConnectionError('сеть недоступна')
        return 'ok'

    flaky.calls = 0
    return flaky


def test_returns_result_on_first_success():
    func = make_flaky(0)
    decorated = retry(times=3, exceptions=(ConnectionError,), sleep=no_sleep)(func)

    assert decorated() == 'ok'
    assert func.calls == 1


def test_succeeds_after_failures():
    func = make_flaky(2)
    decorated = retry(times=3, exceptions=(ConnectionError,), sleep=no_sleep)(func)

    assert decorated() == 'ok'
    assert func.calls == 3


def test_gives_up_after_times_attempts():
    func = make_flaky(3)
    decorated = retry(times=3, exceptions=(ConnectionError,), sleep=no_sleep)(func)

    with pytest.raises(ConnectionError):
        decorated()
    assert func.calls == 3


def test_waits_with_backoff():
    waits = []
    func = make_flaky(10)
    decorated = retry(times=4, exceptions=(ConnectionError,), delay=1, backoff=2,
                      sleep=waits.append)(func)

    with pytest.raises(ConnectionError):
        decorated()
    assert waits == [1, 2, 4]


def test_other_exceptions_are_not_retried():
    calls = 0

    @retry(times=3, exceptions=(ConnectionError,), sleep=no_sleep)
    def broken():
        nonlocal calls
        calls += 1
        raise ValueError('плохие данные')

    with pytest.raises(ValueError):
        broken()
    assert calls == 1


def test_keeps_function_name():
    @retry(times=3, exceptions=(ConnectionError,), sleep=no_sleep)
    def fetch_data():
        """Документация"""

    assert fetch_data.__name__ == 'fetch_data'
    assert fetch_data.__doc__ == 'Документация'