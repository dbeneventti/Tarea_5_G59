import streamlit as st
import pandas as pd
from datetime import date

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/dbeneventti/Tarea_5_G59/main/data.csv", parse_dates=["Date"])

# Título del dashboard
st.title("📊 Dashboard Ventas - Grupo 59")

# ---------------------------
# Filtros
# ---------------------------
with st.expander("🔍 Filtros", expanded=False):
    col1, col2, col3, col4, col5 = st.columns(5)

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

    st.markdown("---")

    # Filtro de fechas con slider (segunda fila)
    col6, _ = st.columns([2, 3])  # más espacio a la izquierda
    with col6:
        fecha_min = df["Date"].min().date()
        fecha_max = df["Date"].max().date()
        fecha_inicio, fecha_fin = st.slider(
            "Selecciona el rango de fechas",
            min_value=fecha_min,
            max_value=fecha_max,
            value=(fecha_min, fecha_max),
            format="DD/MM/YYYY"
        )

# ---------------------------
# Filtrar datos
# ---------------------------
df_filtrado = df[
    (df["City"].isin(ciudades_sel)) &
    (df["Gender"].isin(generos_sel)) &
    (df["Payment"].isin(pagos_sel)) &
    (df["Product line"].isin(productos_sel)) &
    (df["Customer type"].isin(clientes_sel)) &
    (df["Date"].dt.date >= fecha_inicio) &
    (df["Date"].dt.date <= fecha_fin)
]

# ---------------------------
# Mostrar resultados
# ---------------------------
st.subheader("📋 Datos filtrados")
st.dataframe(df_filtrado)

