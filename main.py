from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel


class Item(BaseModel):
    text: str


app = FastAPI()
classifier = pipeline("sentiment-analysis")


@app.get("/")
def root():
    return {'message': "FastApi service started!"}


@app.get("/{text}")
def get_params(text: str):
    try:
        return classifier(text)
    except:
        return {'message': 'Ошибка классификации'}


@app.post("/predict/")
def predict(item: Item):
    return classifier(item.text)
