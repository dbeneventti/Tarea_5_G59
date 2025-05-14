import streamlit as st

st.title("¡Hola, Streamlit! 👋")
st.write("Esta es mi primera app desplegada en Streamlit Cloud.")

x = st.slider("Selecciona un valor", 0, 100, 50)
st.write("Has seleccionado:", x)