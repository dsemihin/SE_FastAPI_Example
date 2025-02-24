from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

class Item(BaseModel):
    text: str

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.get("/")
def root():
    """Корневой эндпоинт для подтверждения работы сервиса."""
    return {"сообщение": "Сервис FastAPI запущен!"}

@app.get("/{text}")
def get_params(text: str):
    """Эндпоинт для получения анализа тональности текста."""
    return classifier(text)

@app.post("/predict/")
def predict(item: Item):
    """Эндпоинт для предсказания тональности текста."""
    return classifier(item.text)