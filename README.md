# Decotators kit

библиотека полезных декораторов для Python:

- `retry` — повторяет вызов функции при заданных исключениях, с растущей задержкой между попытками;
- `memoize` — кеширует результаты функции навсегда;
- `timed_cache` — кеширует результаты на `ttl` секунд;
- `rate_limit` — ограничивает число вызовов за период и выбрасывает `RateLimitExceeded` при превышении.

---
## Запуск тестов
```bash
python -m venv venv
source venv\Scripts\activate
pip install pytest
python -m pytest
```

