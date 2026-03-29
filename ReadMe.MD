ReadMe
# Sentiment Analysis Service

A simple sentiment analysis service built with FastAPI and Streamlit.

## Requirements

pip install fastapi transformers streamlit uvicorn torch requests

## Run API

uvicorn main:app --reload

API will be available at: http://localhost:8000

## Run Web UI

streamlit run app.py

Web interface will be available at: http://localhost:8501

## API Endpoints

- GET / — health check
- GET /{text} — analyze text via URL parameter
- POST /predict/ — analyze text via request body

### Example request

curl -X POST http://localhost:8000/predict/ \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this product!"}'

### Example response

[{"label": "POSITIVE", "score": 0.9998}]