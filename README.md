# Запуск проекта

## Требования

- Python 3.14+
- uv
- Git

## Установка

```bash
git clone https://github.com/AlexZbe/dummyjson-home-work.git
cd dummyjson-home-work
uv sync
```

## Настройка окружения

```bash
cp .env-example .env
```

## Применение миграций

```bash
uv run alembic upgrade head
```

## Запуск приложения

```bash
uv run fastapi dev src/main.py
```

Или через Uvicorn:

```bash
uv run uvicorn src.main:app --reload
```

После запуска:

- приложение: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Остановка

Нажмите:

```text
Ctrl+C
```
