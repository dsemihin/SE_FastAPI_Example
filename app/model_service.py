from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def predict_sentiment(text: str):
    return classifier(text)