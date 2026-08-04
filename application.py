import pandas as pd
import streamlit as st

st.title("Administrador y Visualizador de Tablas de Excel")
st.write(
    "Sube archivos de Excel, visualiza sus hojas y elimina las que desees"
    " usando el botón correspondiente."
)

# Widget para subir archivos
uploaded_files = st.file_uploader(
    "Elige tus archivos de Excel", type=["xlsx", "xls"], accept_multiple_files=True
)

# Inicializar el estado de la sesión para las tablas cargadas
if "loaded_sheets" not in st.session_state:
  st.session_state.loaded_sheets = {}

if uploaded_files:
  # Cargar o actualizar las hojas en la sesión basadas en los archivos subidos
  current_keys = []
  for uploaded_file in uploaded_files:
    try:
      excel_file = pd.ExcelFile(uploaded_file)
      for sheet_name in excel_file.sheet_names:
        key = f"{uploaded_file.name} - Hoja: {sheet_name}"
        current_keys.append(key)
        if key not in st.session_state.loaded_sheets:
          df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
          st.session_state.loaded_sheets[key] = df
    except Exception as e:
      st.error(f"Error al procesar el archivo {uploaded_file.name}: {e}")

  # Opcional: limpiar tablas de archivos que ya fueron removidos del uploader
  keys_to_remove = [
      k
      for k in st.session_state.loaded_sheets.keys()
      if not any(k.startswith(f.name) for f in uploaded_files)
  ]
  for k in keys_to_remove:
    del st.session_state.loaded_sheets[k]

# Verificar si hay tablas en memoria
if st.session_state.loaded_sheets:
  st.subheader("Tablas Actuales en Memoria")
  st.write(
      "Puedes eliminar cualquier tabla haciendo clic en el botón rojo"
      " correspondiente."
  )

  # Creamos una copia de las claves para iterar de forma segura mientras modificamos el diccionario
  for key, df in list(st.session_state.loaded_sheets.items()):
    col1, col2 = st.columns([4, 1])

    with col1:
      st.markdown(f"**{key}**")
      st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

    with col2:
      # Botón único por tabla para eliminarla inmediatamente sin conflictos de estado
      if st.button("Borrar", key=f"del_{key}"):
        del st.session_state.loaded_sheets[key]
        st.rerun()

    st.dataframe(df)
    st.divider()
else:
  st.info(
      "No hay tablas cargadas. Por favor, sube uno o varios archivos de Excel."
  )
