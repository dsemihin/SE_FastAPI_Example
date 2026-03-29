from fastapi import FastAPI
from pydantic import BaseModel
from app.model_service import predict_sentiment


class Item(BaseModel):
    text: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI service started!"}


@app.get("/{text}")
def get_params(text: str):
    return predict_sentiment(text)


@app.post("/predict/")
def predict(item: Item):
    return predict_sentiment(item.text)