import pandas as pd
import streamlit as st

st.title("Visualizador de Archivos de Excel")
st.write(
    "Sube uno o varios archivos de Excel (.xlsx o .xls) para ver su contenido en tablas."
)

# Widget para subir archivos (permite múltiples archivos)
uploaded_files = st.file_uploader(
    "Elige tus archivos de Excel", type=["xlsx", "xls"], accept_multiple_files=True
)

if uploaded_files:
  for uploaded_file in uploaded_files:
    st.subheader(f"Archivo: {uploaded_file.name}")

    try:
      # Leer el archivo de Excel usando pandas
      df = pd.read_excel(uploaded_file)

      # Mostrar las dimensiones del DataFrame
      st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

      # Mostrar la tabla interactiva
      st.dataframe(df)

      st.divider()

    except Exception as e:
      st.error(f"Ocurrió un error al leer el archivo {uploaded_file.name}: {e}")
else:
  st.info("Esperando a que subas al menos un archivo de Excel.")
