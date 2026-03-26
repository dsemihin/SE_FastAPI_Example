import streamlit as st
import requests
from PIL import Image
import io

 
st.title("Streamlit интерфейс для DeepFace")

# Функционал загрузки изображений 
uploaded_file = st.file_uploader("Выберите фото для анализа", type=["jpg", 
"png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Визуализация результатов (само изображение) [cite: 63]
    st.image(image, caption="Загруженное изображение", 
use_column_width=True)
    
    if st.button("Запустить анализ"):
        with st.spinner('Связь с API...'):
            try:
                # Подключение к API (http://localhost:8000) 
                files = {"file": uploaded_file.getvalue()}
                response = requests.post("http://localhost:8000/analyze", 
files=files)
                
                if response.status_code == 200:
                    st.success("Готово!")
                    # Визуализация ответа от модели [cite: 63]
                    st.json(response.json())
                else:
                    st.error(f"Ошибка сервера: {response.status_code}")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
