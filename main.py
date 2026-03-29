from fastapi import FastAPI, HTTPException
from transformers import pipeline
from pydantic import BaseModel


class Item(BaseModel):
    text: str


app = FastAPI()
classifier = pipeline("sentiment-analysis")


@app.get("/")
def root():
    return {"FastApi service started!"}


@app.get("/{text}")
def get_params(text: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return classifier(text)


@app.post("/predict/")
def predict(item: Item):
    if not item.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return classifier(item.text)