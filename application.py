import pandas as pd
import streamlit as st

st.title("Administrador y Visualizador de Tablas de Excel")
st.write(
    "Sube tus archivos de Excel. Selecciona las casillas de las tablas que"
    " deseas eliminar y presiona el botón de borrado."
)

# Widget para subir archivos
uploaded_files = st.file_uploader(
    "Elige tus archivos de Excel", type=["xlsx", "xls"], accept_multiple_files=True
)

# Inicializar la memoria de sesión si no existe
if "loaded_sheets" not in st.session_state:
  st.session_state.loaded_sheets = {}

# Procesar archivos subidos unicamente si hay archivos nuevos
if uploaded_files:
  current_file_names = {f.name for f in uploaded_files}

  # Cargar hojas nuevas
  for uploaded_file in uploaded_files:
    try:
      excel_file = pd.ExcelFile(uploaded_file)
      for sheet_name in excel_file.sheet_names:
        key = f"{uploaded_file.name} -> {sheet_name}"
        # Si la tabla no está en memoria, la cargamos
        if key not in st.session_state.loaded_sheets:
          df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
          st.session_state.loaded_sheets[key] = df
    except Exception as e:
      st.error(f"Error al leer {uploaded_file.name}: {e}")

  # Remover de la memoria los archivos que el usuario borró del uploader
  keys_to_drop = []
  for key in st.session_state.loaded_sheets.keys():
    file_name_in_key = key.split(" -> ")[0]
    if file_name_in_key not in current_file_names:
      keys_to_drop.append(key)
  for k in keys_to_drop:
    del st.session_state.loaded_sheets[k]

else:
  # Si se borraron todos los archivos del uploader, limpiamos la memoria por completo
  st.session_state.loaded_sheets = {}

# Mostrar las tablas y permitir su eliminación
if st.session_state.loaded_sheets:
  st.subheader("Tablas en Memoria")

  # Crear una lista de control para seleccionar qué borrar
  selection_data = []
  for key in list(st.session_state.loaded_sheets.keys()):
    selection_data.append({"Seleccionar": False, "Tabla / Hoja": key})

  df_selection = pd.DataFrame(selection_data)

  # Usar un editor de datos interactivo para marcar con palomitas de forma segura
  edited_df = st.data_editor(
      df_selection,
      column_config={
          "Seleccionar": st.column_config.CheckboxColumn(
              "Borrar?",
              help="Marca la casilla de la tabla que deseas eliminar",
              default=False,
          )
      },
      disabled=["Tabla / Hoja"],
      hide_index=True,
      use_container_width=True,
  )

  # Botón para aplicar el borrado de las filas marcadas
  if st.button("Eliminar tablas seleccionadas"):
    # Obtener las claves que tienen la casilla marcada como True
    keys_to_delete = edited_df.loc[
        edited_df["Seleccionar"] == True, "Tabla / Hoja"
    ].tolist()

    if keys_to_delete:
      for key in keys_to_delete:
        if key in st.session_state.loaded_sheets:
          del st.session_state.loaded_sheets[key]
      st.success("Tablas eliminadas exitosamente.")
      st.rerun()
    else:
      st.warning("No seleccionaste ninguna tabla para borrar.")

  st.divider()

  # Mostrar el contenido visual de cada tabla restante
  for key, df in st.session_state.loaded_sheets.items():
    st.markdown(f"**Visualizando: {key}**")
    st.write(f"Dimensiones -> Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    st.dataframe(df)
    st.divider()

else:
  st.info("Sube uno o varios archivos de Excel para comenzar.")
