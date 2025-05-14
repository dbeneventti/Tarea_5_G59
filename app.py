import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import date

# Configuración de página
st.set_page_config(layout="wide")

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/dbeneventti/Tarea_5_G59/main/data.csv", parse_dates=["Date"])

# Título
st.title("📊 Dashboard Ventas - Grupo 59")

# Filtros (todo en la primera fila)
with st.expander("🔍 Filtros", expanded=False):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        ciudades_sel = st.multiselect("Ciudad", df["City"].unique(), default=df["City"].unique())

    with col2:
        generos_sel = st.multiselect("Género", df["Gender"].unique(), default=df["Gender"].unique())

    with col3:
        pagos_sel = st.multiselect("Pago", df["Payment"].unique(), default=df["Payment"].unique())

    with col4:
        productos_sel = st.multiselect("Producto", df["Product line"].unique(), default=df["Product line"].unique())

    with col5:
        clientes_sel = st.multiselect("Cliente", df["Customer type"].unique(), default=df["Customer type"].unique())

    with col6:
        fecha_min = df["Date"].min().date()
        fecha_max = df["Date"].max().date()
        fecha_inicio, fecha_fin = st.slider(
            "Fecha",
            min_value=fecha_min,
            max_value=fecha_max,
            value=(fecha_min, fecha_max),
            format="DD/MM/YYYY"
        )

# Aplicar filtros
df_filtrado = df[
    (df["City"].isin(ciudades_sel)) &
    (df["Gender"].isin(generos_sel)) &
    (df["Payment"].isin(pagos_sel)) &
    (df["Product line"].isin(productos_sel)) &
    (df["Customer type"].isin(clientes_sel)) &
    (df["Date"].dt.date >= fecha_inicio) &
    (df["Date"].dt.date <= fecha_fin)
]

# -----------------------
# FILA 1 DE GRÁFICOS (3)
# -----------------------
col1, col2, col3 = st.columns(3)

# Gráfico 1: Evolución de ventas
with col1:
    st.subheader("📈 Evolución de Ventas")
    ventas_diarias = df_filtrado.groupby("Date")["Total"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=ventas_diarias, x="Date", y="Total", marker="o", ax=ax1)
    ax1.set_title("Ventas Totales por Fecha")
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Total")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)

# Gráfico 2: Ingresos por línea de producto
with col2:
    st.subheader("🛍️ Ventas por Producto")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_filtrado, x="Product line", y="Total", estimator=sum, errorbar=None, ax=ax2)
    ax2.set_title("Ingresos por Línea de Producto")
    ax2.set_xlabel("")
    ax2.set_ylabel("Total Ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

# Gráfico 3: Distribución de rating
with col3:
    st.subheader("⭐ Distribución de Calificaciones")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.histplot(df_filtrado["Rating"], bins=20, kde=True, color="skyblue", ax=ax3)
    ax3.set_title("Distribución de Ratings")
    ax3.set_xlabel("Calificación")
    ax3.set_ylabel("Frecuencia")
    ax3.grid(False)
    plt.tight_layout()
    st.pyplot(fig3)

