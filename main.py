from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml_model import SentimentAnalyzer

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0.0"
)

class Item(BaseModel):
    text: str

# Инициализация модели
analyzer = SentimentAnalyzer()

@app.get("/")
def root():
    return {"status": "ok", "service": "Sentiment Analysis API"}


@app.post("/predict/")
def predict(item: Item):
    try:
        if not item.text or not item.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = analyzer.predict(item.text)
        
        return {
            "text": item.text,
            "label": result['label'],
            "score": round(result['score'], 4)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)