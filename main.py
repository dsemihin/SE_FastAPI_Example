from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

class Item(BaseModel):
    text: str

app = FastAPI(title="API для анализа сентимента", description="API для анализа сентимента с использованием Hugging Face Transformers.", version="1.0")

# Создаем классификатор для анализа сентимента
classifier = pipeline("sentiment-analysis")

@app.get("/")
def root():
    """Корневой эндпоинт для проверки работоспособности сервиса."""
    return {"message": "Сервис FastAPI запущен!"}

@app.get("/labels/")
def get_labels():
    """Получить доступные метки для анализа сентимента."""
    return {"labels": classifier.model.config.id2label}

@app.get("/{text}")
def get_params(text: str):
    """Анализировать сентимент переданного текста.

    Args:
        text (str): Текст для анализа.

    Returns:
        dict: Результат анализа сентимента.
    """
    return classifier(text)

@app.post("/predict/")
def predict(item: Item):
    """Предсказать сентимент для переданного текста в формате JSON.

    Args:
        item (Item): Входной объект, содержащий текст для анализа.

    Returns:
        dict: Результат анализа сентимента.
    """
    return classifier(item.text)
