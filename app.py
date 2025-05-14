import streamlit as st
import pandas as pd

df = pd.read_csv("https://github.com/dbeneventti/Tarea_5_G59/blob/main/data.csv", parse_dates=["Date"])

st.title("Dashboard Ventas - Grupo 59")

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    ciudad = st.selectbox("Ciudad", df["City"].unique())

with col2:
    genero = st.multiselect("Género", df["Gender"].unique(), default=df["Gender"].unique())

with col3:
    metodo_pago = st.multiselect("Método de Pago", df["Payment"].unique(), default=df["Payment"].unique())


df_filtrado = df[
    (df["City"] == ciudad) &
    (df["Gender"].isin(genero)) &
    (df["Payment"].isin(metodo_pago))
]


st.dataframe(df_filtrado)
