# Приложение для sentiment analysis
REST API на основе **FastAPI** и **HuggingFace Transformers** для определения тональности текста.

### Команда
> Хуснутдинов Эдуард Ринатович - Backend

> Эспиноза Хуан Карлос Ортис - Frontend

---


## Запуск приложения

```bash
uvicorn main:app --reload
```

Сервис запустится по адресу `http://localhost:8000`.

Флаг `--reload` включает автоматическую перезагрузку при изменении кода — удобно для разработки. В продакшене его лучше убрать.

## Эндпоинты

### `GET /`
Проверка работоспособности сервиса.

```bash
curl http://localhost:8000/
```

Ответ:
```json
["FastApi service started!"]
```

---

### `GET /{text}`
Анализ тональности текста, переданного прямо в URL.

```bash
curl "http://localhost:8000/I%20love%20this%20product"
```

> Пробелы в URL нужно заменять на `%20`.

---

### `POST /predict/`
Анализ тональности текста, переданного в теле запроса.

```bash
curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this product"}'
```

Ответ:
```json
[{ "label": "POSITIVE", "score": 0.9998 }]
```


## Документация

FastAPI автоматически генерирует интерактивную документацию:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
