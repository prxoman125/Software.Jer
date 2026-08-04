import io
import zipfile
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
    page_title="Lector y Traductor Corporativo Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# ESTILOS CORPORATIVOS AVANZADOS (SaaS Clean Theme)
# ==========================================
st.markdown(
    """
    <style>
        /* Estilos generales corporativos limpios y minimalistas */
        .main {
            background-color: #0f172a;
            color: #f8fafc;
        }

        /* Encabezado Principal Corporativo */
        .header-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .header-title {
            color: #f8fafc !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            margin: 0 0 8px 0 !important;
            letter-spacing: -0.5px;
        }
        .header-subtitle {
            color: #94a3b8 !important;
            font-size: 15px !important;
            margin: 0 !important;
            font-weight: 400;
        }

        /* Tarjetas de Contenedores de Tablas */
        .table-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }

        /* Paneles laterales / Configuración */
        .css-1d391kg, [data-testid="stSidebar"] {
            background-color: #0b0f19;
            border-right: 1px solid #1e293b;
        }

        /* Botones de acción profesionales */
        div.stButton > button {
            width: 100% !important;
            height: 44px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: 1px solid #334155 !important;
            transition: all 0.2s ease-in-out !important;
        }
        div.stButton > button:hover {
            border-color: #38bdf8 !important;
            background-color: #334155 !important;
        }

        /* Tablas Streamlit */
        [data-testid="stDataFrame"] {
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            background-color: #0f172a !important;
        }
    </style>""",
    unsafe_allow_html=True,
)

# Inicializar estados de sesión de forma segura y estructurada
if "tablas_originales" not in st.session_state:
  st.session_state.tablas_originales = {}  # {nombre_archivo: {sheet_name: df}}
if "tablas_render" not in st.session_state:
  st.session_state.tablas_render = {}  # {nombre_archivo: {sheet_name: df}}
if "idioma_actual" not in st.session_state:
  st.session_state.idioma_actual = "Original"
if "uploader_key" not in st.session_state:
  st.session_state.uploader_key = 0


def hacer_columnas_unicas(df: pd.DataFrame) -> pd.DataFrame:
  """Asegura que los nombres de las columnas sean únicos agregando sufijos si hay duplicados."""
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


def convertir_df_a_excel(df: pd.DataFrame) -> bytes:
  """Convierte un DataFrame a formato Excel (.xlsx) en memoria."""
  output = io.BytesIO()
  with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Datos_Procesados")
  return output.getvalue()


def crear_zip_masivo(tablas_dict: dict) -> bytes:
  """Comprime múltiples DataFrames procesados en un archivo ZIP en memoria."""
  zip_buffer = io.BytesIO()
  with zipfile.ZipFile(
      zip_buffer, "w", zipfile.ZIP_DEFLATED
  ) as zip_file_obj:
    for nombre_archivo, sheets in tablas_dict.items():
      for sheet_name, df in sheets.items():
        excel_data = convertir_df_a_excel(df)
        nombre_dentro_zip = f"traducido_{nombre_archivo.replace('.xlsx', '')}_{sheet_name}.xlsx"
        zip_file_obj.writestr(nombre_dentro_zip, excel_data)
  return zip_buffer.getvalue()


# ==========================================
# INTERFAZ PRINCIPAL - HEADER
# ==========================================
st.markdown(
    """
    <div class="header-container">
        <h1 class="header-title">📊 Lector y Traductor Multitabla Corporativo</h1>
        <p class="header-subtitle">Plataforma avanzada de procesamiento, traducción optimizada y gestión inteligente de datos empresariales en Excel.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# BARRA LATERAL - CONFIGURACIÓN Y CARGA
# ==========================================
with st.sidebar:
  st.markdown("### 📂 Carga de Archivos")
  uploaded_files = st.file_uploader(
      "Selecciona archivos Excel (.xlsx)",
      type=["xlsx"],
      accept_multiple_files=True,
      key=f"uploader_{st.session_state.uploader_key}",
  )

  st.markdown("---")
  st.markdown("### ⚙️ Parámetros de Traducción")
  idioma_seleccionado = st.selectbox(
      "Dirección de Traducción",
      ("Español (desde Inglés)", "Inglés (desde Español)"),
      index=0,
  )

  excluir_numericas = st.checkbox(
      "Excluir automáticamente columnas numéricas/IDs",
      value=True,
      help=(
          "Evita enviar números de serie, fechas o identificadores al traductor"
          " para mejorar la velocidad y precisión."
      ),
  )

  st.markdown("---")
  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    btn_traducir = st.button("🚀 Traducir", type="primary")
  with col_btn2:
    btn_borrar = st.button("🧹 Limpiar")

# ==========================================
# GESTIÓN DE CARGA DE DATOS EN MEMORIA
# ==========================================
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
          xls = pd.ExcelFile(file)
          sheets_dict = {}
          sheets_render_dict = {}
          for sheet in xls.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet)
            if not df.empty:
              df = hacer_columnas_unicas(df)
              sheets_dict[sheet] = df.copy()
              sheets_render_dict[sheet] = df.copy()
          if sheets_dict:
            nuevos_originales[file.name] = sheets_dict
            nuevos_render[file.name] = sheets_render_dict
        except Exception as e:
          st.sidebar.error(f"Error al leer {file.name}: {e}")

    st.session_state.tablas_originales = nuevos_originales
    st.session_state.tablas_render = nuevos_render
    st.session_state.idioma_actual = "Original"

# Lógica del Botón Limpiar
if btn_borrar:
  st.session_state.tablas_originales = {}
  st.session_state.tablas_render = {}
  st.session_state.idioma_actual = "Original"
  st.session_state.uploader_key += 1
  st.rerun()

# ==========================================
# LÓGICA DE TRADUCCIÓN OPTIMIZADA CON BARRA DE PROGRESO
# ==========================================
if btn_traducir and st.session_state.tablas_originales:
  target_lang = "es" if "Español" in idioma_seleccionado else "en"
  source_lang = "en" if target_lang == "es" else "es"

  try:
    translator = GoogleTranslator(source=source_lang, target=target_lang)

    total_celdas_aprox = 0
    for f_name, sheets in st.session_state.tablas_originales.items():
      for s_name, df in sheets.items():
        total_celdas_aprox += df.shape[0] * df.shape[1]

    progress_bar = st.progress(0)
    status_text = st.empty()
    celdas_procesadas = 0

    def traducir_seguro(val):
      if pd.isna(val):
        return val
      val_str = str(val).strip()
      if val_str and not val_str.replace(".", "", 1).isdigit():
        try:
          res = translator.translate(val_str)
          return res if res else val
        except Exception:
          return val
      return val

    nuevos_render_traducidos = {}

    for nombre_archivo, sheets in st.session_state.tablas_originales.items():
      sheets_traducidas = {}
      for sheet_name, df_orig in sheets.items():
        df_traducido = df_orig.copy()

        # 1. Traducir Encabezados
        nuevas_cols = []
        for col in df_traducido.columns:
          col_str = str(col).strip()
          if col_str and not col_str.isdigit():
            try:
              res_col = translator.translate(col_str)
              nuevas_cols.append(res_col if res_col else col_str)
            except Exception:
              nuevas_cols.append(col_str)
          else:
            nuevas_cols.append(col_str)
        df_traducido.columns = nuevas_cols
        df_traducido = hacer_columnas_unicas(df_traducido)

        # 2. Traducir Celdas por columnas
        for col in df_traducido.columns:
          if excluir_numericas and pd.api.types.is_numeric_dtype(
              df_traducido[col]
          ):
            continue

          df_traducido[col] = (
              df_traducido[col].astype(object).apply(traducir_seguro)
          )
          celdas_procesadas += len(df_traducido)
          if total_celdas_aprox > 0:
            progreso_actual = min(
                float(celdas_procesadas / total_celdas_aprox), 1.0
            )
            progress_bar.progress(progreso_actual)
            status_text.text(
                f"Traduciendo archivo: {nombre_archivo} (Hoja: {sheet_name})..."
            )

        sheets_traducidas[sheet_name] = df_traducido
      nuevos_render_traducidos[nombre_archivo] = sheets_traducidas

    st.session_state.tablas_render = nuevos_render_traducidos
    st.session_state.idioma_actual = (
        "Traducido al Español" if target_lang == "es" else "Traducido al Inglés"
    )

    progress_bar.empty()
    status_text.empty()
    st.success("¡Traducción masiva completada exitosamente!")
    st.rerun()

  except Exception as ex:
    st.error(
        f"Se interrumpió el proceso de traducción por un error de conexión: {ex}"
    )

# ==========================================
# CUERPO PRINCIPAL - VISUALIZACIÓN Y MÉTRICAS
# ==========================================
if st.session_state.tablas_originales:
  st.markdown("### 📥 Panel de Exportación Masiva")
  zip_bytes = crear_zip_masivo(st.session_state.tablas_render)
  st.download_button(
      label="📦 Descargar Todos los Archivos Procesados (.ZIP)",
      data=zip_bytes,
      file_name="archivos_excel_traducidos.zip",
      mime="application/zip",
      type="primary",
  )

  st.markdown("---")
  st.markdown(
      f"#### 🔍 Vista de Datos | Estado: **{st.session_state.idioma_actual}**"
  )

  for nombre_archivo, sheets in st.session_state.tablas_render.items():
    st.markdown(
        f"<h3 style='color: #38bdf8; font-size: 20px; margin-top: 25px;'>📁 Archivo: {nombre_archivo}</h3>",
        unsafe_allow_html=True,
    )

    # CORRECCIÓN DE SELECCIÓN DE HOJAS
    sheet_names = list(sheets.keys())
    if len(sheet_names) > 1:
      sheet_seleccionada = st.selectbox(
          f"Seleccionar Hoja para '{nombre_archivo}':",
          sheet_names,
          key=f"sheet_select_{nombre_archivo}",
      )
    else:
      sheet_seleccionada = sheet_names[0]

    # Obtenemos el DataFrame de forma segura
    df_tabla = sheets[sheet_seleccionada]

    # Panel Métricas Básicas (st.metric)
    total_filas, total_columnas = df_tabla.shape
    celdas_vacias = int(df_tabla.isna().sum().sum())

    m1, m2, m3 = st.columns(3)
    with m1:
      st.metric(label="Total de Filas", value=f"{total_filas:,}")
    with m2:
      st.metric(label="Total de Columnas", value=f"{total_columnas:,}")
    with m3:
      st.metric(label="Celdas Vacías", value=f"{celdas_vacias:,}")

    # Buscador / Filtro en tiempo real
    busqueda = st.text_input(
        f"🔍 Buscar registros en '{nombre_archivo}' -> '{sheet_seleccionada}':",
        key=f"search_{nombre_archivo}_{sheet_seleccionada}",
        placeholder="Escribe para filtrar filas en tiempo real...",
    )

    df_filtrado = df_tabla.copy()
    if busqueda:
      mask = df_filtrado.astype(str).apply(
          lambda col: col.str.contains(busqueda, case=False, na=False)
      ).any(axis=1)
      df_filtrado = df_filtrado[mask]

    # Renderizado de Tabla con Contenedor Profesional Estilizado
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.dataframe(df_filtrado, use_container_width=True, height=350)
    st.markdown("</div>", unsafe_allow_html=True)

    # Botón de descarga individual por hoja/tabla
    excel_data_single = convertir_df_a_excel(df_filtrado)
    nombre_salida = f"traducido_{nombre_archivo.replace('.xlsx', '')}_{sheet_seleccionada}.xlsx"

    st.download_button(
        label=f"📥 Descargar Hoja '{sheet_seleccionada}' en Excel",
        data=excel_data_single,
        file_name=nombre_salida,
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        key=f"download_{nombre_archivo}_{sheet_seleccionada}",
    )
    st.markdown("---")

else:
  st.info(
      "💡 Para comenzar, utiliza el panel lateral izquierdo para subir uno o"
      " varios archivos con formato Excel (.xlsx)."
  )
