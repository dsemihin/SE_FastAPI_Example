# Sentiment Analysis API

Проект является Fork продолжением репозитория великого человека: https://github.com/dsemihin/SE_FastAPI_Example
Представляет собой сервис для анализа текста. На текущий момент содержит только backend FastAPI часть.

## Фичи

- Проверка работоспособности сервиса (health check)
- `GET`-запрос на анализ семантики текста
- `POST`-запрос на анализ семантики текста

## Структура проекта

- `main.py` - FastAPI application entry point

## Установка зависимостей 

Мне если что лень делать requirements.txt я не буду нет не просите
```bash
pip install fastapi uvicorn transformers torch pydantic
```

## Запуск Backend-а

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## API

### `GET /`

Хелс-чек, проверка того, что сервер работает.

Ожидаемый ответ:

```json
{"FastApi service started!"}
```

### `GET /{text}`

Семантически анализирует `{text}`. Выдает оценку - либо POSITIVE, либо NEGATIVE `(label)` и степень уверенности `(score)` (от 0.5 до 1.0).

Пример:

```bash
curl http://127.0.0.1:8000/Hello
```

### `POST /predict/`

То же самое, что и `GET /{text}`, но вместо аргумента в URL, принимает аргумент `{text}` в теле запроса.

Пример:

```bash
curl -X POST http://127.0.0.1:8000/predict/ ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Damn I want to eat so badly\"}"
```

## Пример вывода

```json
[
  {
    "label": "POSITIVE",
    "score": 0.9998
  }
]
```
