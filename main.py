from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from transformers import pipeline
from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    text: str


class PredictionResult(BaseModel):
    label: str
    score: float


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models["classifier"] = pipeline("sentiment-analysis")
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"FastApi service started!"}


@app.get("/{text}")
def get_params(text: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return ml_models["classifier"](text)


@app.post("/predict/", response_model=List[PredictionResult])
def predict(item: Item):
    if not item.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return ml_models["classifier"](item.text)