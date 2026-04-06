import logging
from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

class Item(BaseModel):
    text: str

app = FastAPI()

logger.info("Initializing sentiment-analysis pipeline...")
classifier = pipeline("sentiment-analysis")
logger.info("Model loaded successfully")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "status": "FastApi service started!",
        "model_type": classifier.model.config.model_type,
        "model_name": classifier.model.config._name_or_path,
    }

@app.get("/{text}")
def get_params(text: str):
    logger.info(f"GET prediction for: {text}")
    return classifier(text)

@app.post("/predict/")
def predict(item: Item):
    logger.info(f"POST prediction for text length: {len(item.text)}")
    prediction = classifier(item.text)
    logger.info(f"Result: {prediction}")
    return prediction
