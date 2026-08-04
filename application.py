import io
import pandas as pd
from deep_translator import GoogleTranslator
from requests import Session
import streamlit as st

# ==========================================
# PARCHE DE SEGURIDAD AVANZADO DE CONEXIÓN
# ==========================================
_original_send = Session.send


def _patched_send(*args, **kwargs):
  request = args
  request.headers["User-Agent"] = (
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36"
  )
  return _original_send(*args, **kwargs)


Session.send = _patched_send

# ==========================================
# Configuración de la página
# ==========================================
st.set_page_config(
    page_title="Lector y Traductor Multitabla Pro", layout="wide"
)

# ==========================================
# ESTILOS PERSONALIZADOS: NEÓN Y INTERFAZ DIDÁCTICA
# ==========================================
st.markdown(
    """
    <style>
        /* 1. RECUADRO AZUL OSCURO NEÓN PARA EL TÍTULO PRINCIPAL */
        .recuadro-titulo {
            border: 3px solid #0044cc;
            box-shadow: 0 0 20px #0011aa, inset 0 0 10px #000555;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
            background-color: rgba(0, 10, 50, 0.5);
        }
        .texto-titulo {
            color: #00aaff !important;
            font-size: 32px !important;
            font-weight: bold !important;
            text-shadow: 0 0 10px #0044ff !important;
            margin: 0 !important;
        }

        /* 2. RECUADRO NEÓN PARA LOS TÍTULOS DE CADA TABLA */
        .tabla-contenedor {
            border: 2px solid #0033aa;
            box-shadow: 0 0 12px #001188;
            border-radius: 6px;
            padding: 10px 15px;
            margin-top: 20px;
            margin-bottom: 5px;
            background-color: rgba(0, 5, 30, 0.3);
        }
        .tabla-titulo {
            color: #0077ff !important;
            font-weight: bold !important;
            text-shadow: 0 0 5px #002288 !important;
        }

        /* 3. LÍNEAS INTERNAS Y BORDES DE LAS TABLAS DE STREAMLIT */
        [data-testid="stDataFrame"] {
            border: 2px solid #002288 !important;
            border-radius: 6px !important;
            box-shadow: 0 0 8px #001166 !important;
        }

        /* 4. ESTILOS DIDÁCTICOS PARA BOTONES GRANDES PERSONALIZADOS */
        div.stButton > button {
            width: 100% !important;
            height: 55px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
    </style>""",
    unsafe_allow_html=True,
)

# Inicializar las variables de estado de forma persistente
if "tablas_originales" not in st.session_state:
  st.session_state.tablas_originales = {}
if "tablas_render" not in st.session_state:
  st.session_state.tablas_render = {}
if "idioma_actual" not in st.session_state:
  st.session_state.idioma_actual = "Original"


# Función para asegurar que los nombres de las columnas sean únicos
def hacer_columnas_unicas(df):
  cols = []
  count = {}
  for col in df.columns:
    col_str = str(col).strip()
    if col_str in count:
      count[col_str] += 1
      cols.append(f"{col_str}_{count[col_str]}")
    else:
      count[col_str] = 0
      cols.append(col_str)
  df.columns = cols
  return df


# Función para convertir un DataFrame a Excel en memoria (para descargas)
def convertir_df_a_excel(df):
  output = io.BytesIO()
  with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Traducido")
  processed_data = output.getvalue()
  return processed_data


# Título Principal
st.markdown(
    """
    <div class="recuadro-titulo">
        <h1 class="texto-titulo">Lector y Traductor de Multiples Tablas Excel</h1>
    </div>""",
    unsafe_allow_html=True,
)

st.write(
    "Sube tus archivos de Excel en la sección de abajo para visualizarlos,"
    " traducir su contenido y exportarlos."
)

# Clave dinámica para reiniciar por completo el cargador al borrar
if "uploader_key" not in st.session_state:
  st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "Sube uno o varios archivos Excel (.xlsx)",
    type=["xlsx"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}",
)

# === 1. CAPTURA Y CARGA DE DATOS EN MEMORIA ===
if uploaded_files:
  archivos_actuales = [f.name for f in uploaded_files]
  llaves_guardadas = list(st.session_state.tablas_originales.keys())

  if set(archivos_actuales) != set(llaves_guardadas):
    nuevos_originales = {}
    nuevos_render = {}

    for file in uploaded_files:
      if file.name in st.session_state.tablas_originales:
        nuevos_originales[file.name] = st.session_state.tablas_originales[
            file.name
        ]
        nuevos_render[file.name] = st.session_state.tablas_render[file.name]
      else:
        try:
          df = pd.read_excel(file)
          df = hacer_columnas_unicas(df)
          nuevos_originales[file.name] = df.copy()
          nuevos_render[file.name] = df.copy()
        except Exception as e:
          st.error(f"Error al leer el archivo {file.name}: {e}")

    st.session_state.tablas_originales = nuevos_originales
    st.session_state.tablas_render = nuevos_render
    st.session_state.idioma_actual = "Original"

# === 2. PANEL DE INTERFAZ (IDIOMAS Y BOTONES DIDÁCTICOS) ===
if st.session_state.tablas_originales:
  st.write("### Opciones de traducción y limpieza:")

  idioma_seleccionado = st.selectbox(
      "¿A qué idioma deseas cambiar la información de las tablas?",
      ("Español (de ingles)", "Ingles (de espanol)"),
      index=0,
  )

  st.write("")
  col1, col2 = st.columns(2)

  with col1:
    if st.button("PROCESAR Y TRADUCIR TABLAS", type="primary"):
      target_lang = "es" if idioma_seleccionado == "Español (de ingles)" else "en"

      with st.spinner("Traduciendo columnas y filas... Por favor espera..."):
        try:
          translator = GoogleTranslator(source="auto", target=target_lang)

          def traducir_seguro(val):
            if pd.isna(val):
              return val
            val_str = str(val).strip()
            if val_str and not val_str.replace(".", "", 1).isdigit():
              try:
                res = translator.translate(val_str)
                return res if res else val
              except:
                return val
            return val

          for (
              nombre_archivo,
              df_orig,
          ) in st.session_state.tablas_originales.items():
            df_traducido = df_orig.copy()

            # Traducir los encabezados
            nuevas_cols = []
            for col in df_traducido.columns:
              col_str = str(col).strip()
              if col_str and not col_str.isdigit():
                try:
                  res_col = translator.translate(col_str)
                  nuevas_cols.append(res_col if res_col else col_str)
                except:
                  nuevas_cols.append(col_str)
              else:
                nuevas_cols.append(col_str)

            df_traducido.columns = nuevas_cols
            df_traducido = hacer_columnas_unicas(df_traducido)

            # Traducir celdas
            for col in df_traducido.columns:
              df_traducido[col] = (
                  df_traducido[col].astype(object).apply(traducir_seguro)
              )

            st.session_state.tablas_render[nombre_archivo] = df_traducido

          st.session_state.idioma_actual = "Traducido"
          st.rerun()
        except Exception:
          st.error(
              "Hubo un inconveniente con el servidor de idioma. Por favor"
              " intenta nuevamente."
          )

  with col2:
    if st.button("BORRAR Y LIMPIAR PANTALLA", type="secondary"):
      st.session_state.tablas_originales = {}
      st.session_state.tablas_render = {}
      st.session_state.idioma_actual = "Original"
      st.session_state.uploader_key += 1
      st.rerun()

  # === 3. VISTA EN PANTALLA Y DESCARGAS ===
  st.write("---")
  st.write(f"**Estado de los datos mostrados:** {st.session_state.idioma_actual}")

  for indice, (nombre_archivo, df_tabla) in enumerate(
      st.session_state.tablas_render.items()
  ):
    st.markdown(
        f"""
        <div class="tabla-contenedor">
            <span class="tabla-titulo">Tabla {indice + 1}: {nombre_archivo}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    st.dataframe(df_tabla, use_container_width=True)

    # NUEVA FUNCIÓN: Botón de descarga individual para cada tabla procesada
    excel_data = convertir_df_a_excel(df_tabla)
    nombre_salida = f"traducido_{nombre_archivo}"

    st.download_button(
        label=f"📥 Descargar {nombre_archivo} en Excel",
        data=excel_data,
        file_name=nombre_salida,
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        key=f"download_{indice}_{nombre_archivo}",
    )
    st.write("")

else:
  if not uploaded_files and st.session_state.tablas_originales:
    st.session_state.tablas_originales = {}
    st.session_state.tablas_render = {}
    st.session_state.idioma_actual = "Original"
    st.rerun()
  st.info("Por favor, sube uno o varios archivos Excel para comenzar.")
