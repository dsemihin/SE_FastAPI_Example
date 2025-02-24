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
    try:
        classifier(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        print('Запрос выполнен')
    return classifier(text)


@app.post("/predict/")
def predict(item: Item):
    try:
        classifier(item.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        print('Запрос выполнен')
    return classifier(item.text)
