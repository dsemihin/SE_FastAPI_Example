import streamlit as st
import requests
from PIL import Image
import io

# Настройка страницы
st.set_page_config(page_title="AI Face Analyzer", layout="wide")

st.title("🧬 Анализ лиц с помощью DeepFace")
st.markdown("---")

# Боковая панель для настроек (для вида)
st.sidebar.header("Настройки")
api_url = st.sidebar.text_input("URL API", "http://localhost:8000/analyze")

# Основной интерфейс: делим на две колонки
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Загрузка данных")
    uploaded_file = st.file_uploader("Выберите фото (JPG, PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Оригинал изображения", use_container_width=True)

with col2:
    st.subheader("📊 Результаты анализа")

    if uploaded_file is not None:
        if st.button("Запустить нейросеть", use_container_width=True):
            with st.spinner('Анализируем черты лица...'):
                try:
                    files = {"file": uploaded_file.getvalue()}
                    response = requests.post(api_url, files=files)

                    if response.status_code == 200:
                        data = response.json()
                        st.success("Анализ завершен!")

                        # Если API возвращает список (несколько лиц)
                        results = data if isinstance(data, list) else [data]

                        for idx, face in enumerate(results):
                            with st.expander(f"Лицо №{idx + 1}", expanded=True):
                                # Выводим метрики красиво
                                m_col1, m_col2 = st.columns(2)
                                if 'age' in face:
                                    m_col1.metric("Возраст", face['age'])
                                if 'dominant_emotion' in face:
                                    m_col2.metric("Эмоция", face['dominant_emotion'])

                                # Показываем полный JSON для отладки
                                st.write("Полные данные:")
                                st.json(face)
                    else:
                        st.error(f"Ошибка сервера: {response.status_code}")
                except Exception as e:
                    st.error(f"Не удалось подключиться к API: {e}")
    else:
        st.info("Загрузите изображение слева, чтобы увидеть результат.")