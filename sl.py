import streamlit as st
import pandas as pd

# URL набора данных Titanic на Hugging Face
DS_NAME = """https://huggingface.co/datasets/ankislyakov/titanic/resolve/main/titanic_train.csv"""

# 1. Заголовки и текст
st.title("Анализ данных Титаника")

st.write("Задание 1:")
# Слайдер для выбора возраста (0-100 лет, значение по умолчанию 25)
age = st.slider("Возраст:", min_value=0, max_value=100, value=25)
st.write(f"Анализ для возраста {age} лет.")
# Загрузка данных Titanic по URL
titanic = pd.read_csv(
    DS_NAME,
    index_col="PassengerId",
)
# Фильтрация пассажиров младше выбранного возраста
df = titanic[(titanic["Age"] < age)]["Survived"]

# Фильтрация умерших мужчин старше выбранного возраста с группировкой по порту посадки
df = titanic[(titanic["Sex"] == "male") & (titanic["Survived"] == 0) & (titanic["Age"] > age)]
df = df.groupby("Embarked").size().reset_index(name="Count")

st.subheader(
    """Подсчёт количества умерших мужчин старше указанного возраста
    по каждому порту посадки:"""
)

st.dataframe(df)
# Боковая панель с настройками
with st.sidebar:
    st.header("Настройки")
    # Слайдер для порога уверенности модели (0.0-1.0, значение по умолчанию 0.8)
    confidence = st.slider("Порог уверенности модели:", 0.0, 1.0, 0.8)
    st.info(f"Порог уверенности: {confidence}")

st.write("Задание 2:")

# Переключатели для выбора типа статистики
survival_choice = st.radio(
    "Выберите тип статистики:",
    ["Показать выживших", "Показать погибших"],
    horizontal=True,
)

display_choice = st.radio(
    "Выберите способ отображения:",
    ["Показать проценты", "Показать только количество"],
    horizontal=True,
)

# Фильтрация данных в зависимости от выбора пользователя
if survival_choice == "Показать выживших":
    survived_data = titanic[titanic["Survived"] == 1]
    title = "Статистика выживших"
else:
    survived_data = titanic[titanic["Survived"] == 0]
    title = "Статистика погибших"

# Подсчёт мужчин и женщин в отфильтрованных данных
men_count = len(survived_data[survived_data["Sex"] == "male"])
women_count = len(survived_data[survived_data["Sex"] == "female"])
total_count = len(survived_data)

# Расчёт процентов при наличии данных
if total_count > 0:
    men_percentage = (men_count / total_count) * 100
    women_percentage = (women_count / total_count) * 100
else:
    men_percentage = women_percentage = 0

st.subheader(title)

# Отображение результатов в виде процентов или количества
if display_choice == "Показать проценты":
    results_df = pd.DataFrame(
        {
            "Пол": ["Мужчины", "Женщины", "Итого"],
            "Процент": [f"{men_percentage:.1f}%", f"{women_percentage:.1f}%",
                        "100%"],
        }
    )

else:
    results_df = pd.DataFrame(
        {
            "Пол": ["Мужчины", "Женщины", "Итого"],
            "Количество": [men_count, women_count, total_count],
        }
    )

st.table(results_df)
st.info(f"Проанализированы данные {total_count} пассажиров")