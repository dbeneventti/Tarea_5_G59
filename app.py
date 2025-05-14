import streamlit as st
import pandas as pd

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/dbeneventti/Tarea_5_G59/main/data.csv", parse_dates=["Date"])

# Título del dashboard
st.title("📊 Dashboard Ventas - Grupo 59")

# Filtros dentro de un expander
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

# Aplicar filtros
df_filtrado = df[
    df["City"].isin(ciudades_sel) &
    df["Gender"].isin(generos_sel) &
    df["Payment"].isin(pagos_sel) &
    df["Product line"].isin(productos_sel) &
    df["Customer type"].isin(clientes_sel)
]

# Mostrar tabla
st.dataframe(df_filtrado)
