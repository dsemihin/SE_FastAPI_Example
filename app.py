import streamlit as st
import requests

st.title("Sentiment Analysis")
st.write("Enter text below to analyze its sentiment.")

text = st.text_area("Text for analysis:")

if st.button("Analyze"):
    if text.strip():
        response = requests.post(
            "http://localhost:8000/predict/",
            json={"text": text}
        )
        if response.status_code == 200:
            result = response.json()
            label = result[0]["label"]
            score = result[0]["score"]

            st.success(f"**Label:** {label}")
            st.info(f"**Score:** {score:.4f}")
        else:
            st.error(f"API error: {response.status_code}")
    else:
        st.warning("Please enter some text")