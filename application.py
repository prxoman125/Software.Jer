import os
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Archivos Excel", page_icon="📊", layout="wide"
)

st.title("📊 Gestor y Visualizador de Archivos Excel")
st.write(
    "Sube tus archivos de Excel para visualizarlos y administra los archivos almacenados."
)

# Directorio donde se guardarán los archivos subidos
UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- 1. SECCIÓN DE SUBIDA DE ARCHIVOS ---
st.header("1. Subir Archivo Excel")
uploaded_file = st.file_uploader(
    "Elige un archivo de Excel", type=["xlsx", "xls"]
)

if uploaded_file is not None:
  # Guardar el archivo físicamente en el directorio
  file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
  with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

  st.success(f"¡Archivo '{uploaded_file.name}' subido con éxito!")

  # Leer el archivo con pandas y mostrarlo abajo
  try:
    df = pd.read_excel(file_path)
    st.subheader(f"Vista previa de: {uploaded_file.name}")
    st.dataframe(df)
  except Exception as e:
    st.error(f"Error al leer el archivo de Excel: {e}")

# --- 2. SECCIÓN DE ADMINISTRACIÓN Y ELIMINACIÓN DE ARCHIVOS ---
st.markdown("---")
st.header("2. Administrar Archivos Guardados")

# Listar todos los archivos en el directorio de subidas
saved_files = os.listdir(UPLOAD_DIR)

if not saved_files:
  st.info("No hay archivos guardados actualmente.")
else:
  st.write("Selecciona los archivos que deseas eliminar:")

  # Crear un formulario o checkboxes para seleccionar archivos
  files_to_delete = []
  for file_name in saved_files:
    # Usamos un checkbox para cada archivo disponible
    if st.checkbox(file_name, key=file_name):
      files_to_delete.append(file_name)

  # Botón para ejecutar la eliminación
  if st.button("🗑️ Borrar archivos seleccionados", type="primary"):
    if files_to_delete:
      for file_name in files_to_delete:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        try:
          os.remove(file_path)
          st.success(f"Archivo eliminado: {file_name}")
        except Exception as e:
          st.error(f"No se pudo eliminar {file_name}: {e}")
      # Recargar la página para actualizar la lista de archivos
      st.rerun()
    else:
      st.warning("Por favor, selecciona al menos un archivo para borrar.")
