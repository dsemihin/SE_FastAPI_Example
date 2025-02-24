from fastapi import FastAPI, HTTPException
from transformers import pipeline
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        if not text.strip():
            raise HTTPException(status_code=400, detail="Текст не может быть пустым.")
        return classifier(text)
    except Exception as e:
        logger.error(f"Ошибка при анализе: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")

@app.post("/predict/")
def predict(item: Item):
    try:
        if not item.text.strip():
            raise HTTPException(status_code=400, detail="Текст не может быть пустым.")
        return classifier(item.text)
    except Exception as e:
        logger.error(f"Ошибка при анализе: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")