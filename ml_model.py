from transformers import pipeline


class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")

    def predict(self, text: str) -> dict:
        return self.classifier(text)[0]