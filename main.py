from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

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
    return classifier(text)


@app.post("/predict/")
def predict(item: Item):
    return classifier(item.text)
