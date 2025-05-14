import streamlit as st
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/dbeneventti/Tarea_5_G59/main/data.csv", parse_dates=["Date"])

st.title("📊 Dashboard Ventas - Grupo 59")

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    ciudades = df["City"].unique()
    ciudades_sel = st.multiselect("Ciudad", ciudades, default=ciudades)

with col2:
    generos = df["Gender"].unique()
    generos_sel = st.multiselect("Género", generos, default=generos)

with col3:
    pagos = df["Payment"].unique()
    pagos_sel = st.multiselect("Método de Pago", pagos, default=pagos)

# Segundo grupo de filtros (si lo deseas más adelante)
col4, col5 = st.columns(2)

with col4:
    productos = df["Product line"].unique()
    productos_sel = st.multiselect("Línea de producto", productos, default=productos)

with col5:
    clientes = df["Customer type"].unique()
    clientes_sel = st.multiselect("Tipo de Cliente", clientes, default=clientes)

df_filtrado = df[
    df["City"].isin(ciudades_sel) &
    df["Gender"].isin(generos_sel) &
    df["Payment"].isin(pagos_sel) &
    df["Product line"].isin(productos_sel) &
    df["Customer type"].isin(clientes_sel)
]

st.dataframe(df_filtrado)
