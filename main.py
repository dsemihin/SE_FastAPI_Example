from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel


class Item(BaseModel):
    text: str


app = FastAPI()
try:
    model = pipeline("sentiment-analysis")
    logger.info("Модель загружена")
except Exception as e:
    logger.error(f"Модель не загружена: {e}")
    model = None

@app.get("/")
def root():
    return {"FastApi service started!"}


@app.get("/{text}")
def get_params(text: str):
    return classifier(text)


@app.post("/predict/")
def predict(item: Item):
    return classifier(item.text)
