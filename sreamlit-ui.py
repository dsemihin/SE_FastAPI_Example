import streamlit as st
import requests

st.title("😊 Анализ тональности текста")

API_URL = "http://localhost:8000"

text = st.text_area("Введите текст:")

if st.button("Анализировать"):
    if text:
        try:
            response = requests.post(
                f"{API_URL}/predict/",
                json={"text": text}
            )

            if response.status_code == 200:
                result = response.json()

                if result['label'] == 'POSITIVE':
                    st.success(f"😊 Позитивный ({result['score']:.2%})")
                else:
                    st.error(f"😞 Негативный ({result['score']:.2%})")
            else:
                st.error("Ошибка API")

        except:
            st.error("Не удалось подключиться к API")
    else:
        st.warning("Введите текст")