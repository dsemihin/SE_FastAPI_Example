from fastapi import FastAPI
from transformers import pipeline

from Item import Item

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.get("/")
def root():
    return {"FastApi service is available!"}

@app.get("/{text}")
def get_params(text: str):
    return classifier(text)

@app.post("/predict")
def predict(item: Item):
    return classifier(item.text)
