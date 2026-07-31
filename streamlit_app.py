import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -------------------------
# CONFIGURACIÓN
# -------------------------
st.set_page_config(
    page_title="EDA Finanzas",
    layout="wide"
)

st.title("📊 Análisis Exploratorio de Datos Financieros")

st.write(
    """
    Esta aplicación genera datos financieros sintéticos y permite
    realizar un análisis exploratorio de los mismos.
    """
)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.header("Configuración")

n = st.sidebar.slider(
    "Número de registros",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

np.random.seed(42)

# -------------------------
# DATOS SINTÉTICOS
# -------------------------

categorias = [
    "Tecnología",
    "Salud",
    "Finanzas",
    "Retail",
    "Energía"
]

df = pd.DataFrame({

    "Empresa":
        ["Empresa_" + str(i) for i in range(n)],

    "Sector":
        np.random.choice(categorias, n),

    "Ingresos":
        np.random.normal(100000, 20000, n),

    "Gastos":
        np.random.normal(70000, 15000, n),

    "Activos":
        np.random.normal(300000, 50000, n),

    "Empleados":
        np.random.randint(20, 500, n)

})

df["Utilidad"] = df["Ingresos"] - df["Gastos"]

# -------------------------
# MOSTRAR DATOS
# -------------------------

st.header("1. Datos sintéticos")

st.dataframe(df)

# -------------------------
# EDA CUALITATIVO
# -------------------------

st.header("2. Análisis Cualitativo")

conteo = df["Sector"].value_counts()

st.write("Frecuencia por sector")

fig = px.bar(
    x=conteo.index,
    y=conteo.values,
    labels={
        "x":"Sector",
        "y":"Cantidad"
    },
    title="Empresas por sector"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# EDA CUANTITATIVO
# -------------------------

st.header("3. Estadísticas Descriptivas")

st.dataframe(df.describe())

# -------------------------
# HISTOGRAMA
# -------------------------

st.header("4. Distribución de Variables")

variable = st.selectbox(
    "Seleccione una variable",
    [
        "Ingresos",
        "Gastos",
        "Activos",
        "Utilidad",
        "Empleados"
    ]
)

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(df[variable], kde=True, ax=ax)

ax.set_title(f"Distribución de {variable}")

st.pyplot(fig)

# -------------------------
# MATRIZ DE CORRELACIÓN
# -------------------------

st.header("5. Correlación")

corr = df.select_dtypes(include=np.number).corr()

fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(
    corr,
    annot=True,
    cmap="Blues",
    ax=ax
)

st.pyplot(fig)

# -------------------------
# SCATTER
# -------------------------

st.header("6. Relación entre variables")

x = st.selectbox(
    "Variable X",
    ["Ingresos","Gastos","Activos","Utilidad"],
    index=0
)

y = st.selectbox(
    "Variable Y",
    ["Ingresos","Gastos","Activos","Utilidad"],
    index=3
)

fig = px.scatter(
    df,
    x=x,
    y=y,
    color="Sector",
    hover_name="Empresa",
    title=f"{x} vs {y}"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# FILTRO INTERACTIVO
# -------------------------

st.header("7. Interacción del Usuario")

sector = st.multiselect(
    "Seleccione sectores",
    options=df["Sector"].unique(),
    default=df["Sector"].unique()
)

filtrado = df[df["Sector"].isin(sector)]

st.write(f"Registros encontrados: {len(filtrado)}")

st.dataframe(filtrado)

# -------------------------
# KPIs
# -------------------------

st.header("8. Indicadores")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Ingreso promedio",
    f"${df['Ingresos'].mean():,.0f}"
)

c2.metric(
    "Utilidad promedio",
    f"${df['Utilidad'].mean():,.0f}"
)

c3.metric(
    "Total empresas",
    len(df)
)
