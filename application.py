import pandas as pd
import streamlit as st

st.title("Administrador y Visualizador de Tablas de Excel")
st.write(
    "Sube archivos de Excel, selecciona qué hojas deseas conservar y elimina las"
    " que no necesites."
)

# Widget para subir archivos (permite múltiples archivos)
uploaded_files = st.file_uploader(
    "Elige tus archivos de Excel", type=["xlsx", "xls"], accept_multiple_files=True
)

if uploaded_files:
  # Diccionario para almacenar todas las hojas de todos los archivos cargados
  # Usaremos una clave única combinando el nombre del archivo y el nombre de la hoja
  if "loaded_sheets" not in st.session_state:
    st.session_state.loaded_sheets = {}

  # Cargar o actualizar las hojas en la sesión
  current_file_names = [f.name for f in uploaded_files]

  for uploaded_file in uploaded_files:
    try:
      # Leer todas las hojas del archivo Excel como un diccionario
      excel_file = pd.ExcelFile(uploaded_file)
      for sheet_name in excel_file.sheet_names:
        key = f"{uploaded_file.name} - Hoja: {sheet_name}"
        if key not in st.session_state.loaded_sheets:
          # Cargar el contenido de la hoja
          df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
          st.session_state.loaded_sheets[key] = df
    except Exception as e:
      st.error(f"Error al procesar el archivo {uploaded_file.name}: {e}")

  # Verificar si hay tablas cargadas
  if st.session_state.loaded_sheets:
    st.subheader("Selecciona las tablas que deseas ELIMINAR")
    st.write(
        "Marca con una palomita las tablas que quieras borrar de la vista"
        " inferior:"
    )

    # Crear un formulario o contenedor para las casillas de verificación
    sheets_to_delete = []

    # Contenedor con columnas o lista simple para las opciones
    for key in list(st.session_state.loaded_sheets.keys()):
      # Creamos un checkbox para cada tabla disponible
      if st.checkbox(key, value=False):
        sheets_to_delete.append(key)

    # Botón para ejecutar la acción de borrado
    if st.button("Borrar tablas seleccionadas"):
      if sheets_to_delete:
        for key in sheets_to_delete:
          del st.session_state.loaded_sheets[key]
        st.success("Se han eliminado las tablas seleccionadas.")
        st.rerun()
      else:
        st.warning(
            "No has seleccionado ninguna tabla para borrar. Marca al menos una"
            " palomita."
        )

    st.divider()

    # Mostrar las tablas restantes
    st.subheader("Tablas Actuales en Memoria")
    if st.session_state.loaded_sheets:
      for key, df in st.session_state.loaded_sheets.items():
        st.markdown(f"**{key}**")
        st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
        st.dataframe(df)
        st.divider()
    else:
      st.info("No quedan tablas para mostrar.")

else:
  # Limpiar la sesión si no hay archivos cargados
  if "loaded_sheets" in st.session_state:
    st.session_state.loaded_sheets = {}
  st.info("Esperando a que subas al menos un archivo de Excel.")
