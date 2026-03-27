from typing import List

from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel


class Item(BaseModel):
    text: str


class ItemsBatch(BaseModel):
    texts: List[str]


app = FastAPI()
classifier = pipeline("text-classification")


@app.get("/")
def root():
    return {"FastApi service started!"}


@app.get("/{text}")
def get_params(text: str):
    return classifier(text)


@app.post("/predict/")
def predict(item: Item):
    return classifier(item.text)


@app.post("/predict_multiple/")
def predict_batch(items: ItemsBatch):
    results = classifier(items.texts)
    return {"results": results}
