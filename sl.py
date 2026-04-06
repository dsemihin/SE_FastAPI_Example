import streamlit as st
import pandas as pd

# URL del conjunto de datos del Titanic en Hugging Face
DS_NAME = """https://huggingface.co/datasets/ankislyakov/titanic/resolve/main/titanic_train"""

# 1. Títulos y texto
st.title("Análisis de datos del Titanic")

st.write("Tarea 1:")
# Slider para seleccionar la edad (0-100 años, valor inicial 25)
age = st.slider("Edad:", min_value=0, max_value=100, value=25)
st.write(f"Análisis de {age} años.")
# Cargar los datos del Titanic desde la URL
titanic = pd.read_csv(
    DS_NAME,
    index_col="PassengerId",
)
# Filtrar pasajeros menores de la edad seleccionada
df = titanic[(titanic["Age"] < age)]["Survived"]

# Filtrar hombres muertos mayores de la edad seleccionada, agrupados por puerto de embarque
df = titanic[(titanic["Sex"] == "male") & (titanic["Survived"] == 0) & (titanic["Age"] > age)]
df = df.groupby("Embarked").size().reset_index(name="Count")

st.subheader(
    """Contar el número de hombres muertos mayores de la edad
    especificada por cada puerto de embarque:"""
)

st.dataframe(df)
# Barra lateral con configuraciones
with st.sidebar:
    st.header("Configuración")
    # Slider para el umbral de confianza del modelo (0.0-1.0, valor inicial 0.8)
    confidence = st.slider("Umbral de confianza del modelo:", 0.0, 1.0, 0.8)
    st.info(f"Umbral de confianza: {confidence}")

st.write("Tarea 2:")

# Radio buttons para seleccionar el tipo de estadística a mostrar
survival_choice = st.radio(
    "Seleccione el tipo de estadísticas:",
    ["Mostrar supervivientes", "Mostrar muertos"],
    horizontal=True,
)

display_choice = st.radio(
    "Seleccione el método de visualización:",
    ["Mostrar porcentajes", "Mostrar solo cantidad"],
    horizontal=True,
)

# Filtrar datos según la selección del usuario
if survival_choice == "Mostrar supervivientes":
    survived_data = titanic[titanic["Survived"] == 1]
    title = "Estadísticas de supervivientes"
else:
    survived_data = titanic[titanic["Survived"] == 0]
    title = "Estadísticas de muertos"

# Contar hombres y mujeres en los datos filtrados
men_count = len(survived_data[survived_data["Sex"] == "male"])
women_count = len(survived_data[survived_data["Sex"] == "female"])
total_count = len(survived_data)

# Calcular porcentajes si hay datos
if total_count > 0:
    men_percentage = (men_count / total_count) * 100
    women_percentage = (women_count / total_count) * 100
else:
    men_percentage = women_percentage = 0

st.subheader(title)

# Mostrar resultados en formato de porcentaje o cantidad
if display_choice == "Mostrar porcentajes":
    results_df = pd.DataFrame(
        {
            "Género": ["Hombres", "Mujeres", "Total"],
            "Porcentaje": [f"{men_percentage:.1f}%", f"{women_percentage:.1f}%",
                        "100%"],
        }
    )

else:
    results_df = pd.DataFrame(
        {
            "Género": ["Hombres", "Mujeres", "Total"],
            "Cantidad": [men_count, women_count, total_count],
        }
    )

st.table(results_df)
st.info(f"Se analizaron datos de {total_count} pasajeros")