from fastapi import FastAPI, HTTPException
from transformers import pipeline
from pydantic import BaseModel

class Item(BaseModel):
    text: str

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.get("/")
def root():
    return {"message": "FastAPI service started!"}

@app.get("/analyze/{text}")
def analyze_text(text: str):
    try:
        result = classifier(text)
        return {"text": text, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")

@app.post("/predict/")
def predict(item: Item):
    try:
        result = classifier(item.text)
        return {"text": item.text, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")
