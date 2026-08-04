import pandas as pd
import streamlit as st

st.title("Visualizador de Archivos de Excel")
st.write(
    "Sube uno o varios archivos de Excel (.xlsx o .xls) para ver su contenido en tablas."
)

# Inicializar el estado de la sesión para los archivos si no existe
if "uploaded_files_cache" not in st.session_state:
  st.session_state.uploaded_files_cache = None

# Widget para subir archivos
uploaded_files = st.file_uploader(
    "Elige tus archivos de Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    key="file_uploader",
)

# Actualizar la caché si se suben nuevos archivos
if uploaded_files:
  st.session_state.uploaded_files_cache = uploaded_files

# Botón para borrar las tablas generadas
if st.session_state.uploaded_files_cache:
  if st.button("🗑️ Borrar tablas y limpiar"):
    st.session_state.uploaded_files_cache = None
    # Forzar la recarga para limpiar el file_uploader y la pantalla
    st.rerun()

# Mostrar las tablas si hay archivos en la caché
if st.session_state.uploaded_files_cache:
  for uploaded_file in st.session_state.uploaded_files_cache:
    st.subheader(f"Archivo: {uploaded_file.name}")

    try:
      df = pd.read_excel(uploaded_file)
      st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
      st.dataframe(df)
      st.divider()

    except Exception as e:
      st.error(f"Ocurrió un error al leer el archivo {uploaded_file.name}: {e}")
else:
  st.info("Esperando a que subas al menos un archivo de Excel.")
