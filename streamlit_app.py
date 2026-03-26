import streamlit as st
from transformers import pipeline

st.title("Sentiment Analysis App")

classifier = pipeline("sentiment-analysis")

text = st.text_area("Введите текст")

if st.button("Проверить"):
    if text:
        result = classifier(text)
        st.write(result)
    else:
        st.warning("Введите текст")
