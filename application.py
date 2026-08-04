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
# ESTILOS PERSONALIZADOS: ANIMACIÓN NEÓN Y UI MEJORADA
# ==========================================
st.markdown(
    """
    <style>
        /* Animación de luces neón fluidas (azul oscuro a azul medio claro) */
        @keyframes neonPulse {
            0% {
                border-color: #0044cc;
                box-shadow: 0 0 15px #0011aa, inset 0 0 8px #000555;
            }
            50% {
                border-color: #00bfff;
                box-shadow: 0 0 25px #0088ff, inset 0 0 15px #0044aa;
            }
            100% {
                border-color: #0044cc;
                box-shadow: 0 0 15px #0011aa, inset 0 0 8px #000555;
            }
        }

        @keyframes neonGlowSoft {
            0% {
                border-color: #0033aa;
                box-shadow: 0 0 10px #001188;
            }
            50% {
                border-color: #0099ff;
                box-shadow: 0 0 18px #0055cc;
            }
            100% {
                border-color: #0033aa;
                box-shadow: 0 0 10px #001188;
            }
        }

        /* 1. RECUADRO ANIMADO PARA EL TÍTULO PRINCIPAL */
        .recuadro-titulo {
            border: 3px solid #0044cc;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(135deg, rgba(0, 10, 40, 0.7), rgba(0, 30, 80, 0.4));
            animation: neonPulse 6s infinite ease-in-out;
        }
        .texto-titulo {
            color: #e0f7ff !important;
            font-size: 32px !important;
            font-weight: 800 !important;
            text-shadow: 0 0 12px #00bfff, 0 u 0 20px #0044ff !important;
            margin: 0 !important;
            letter-spacing: 1px;
        }

        /* 2. RECUADRO ANIMADO PARA LOS TÍTULOS DE CADA TABLA */
        .tabla-contenedor {
            border: 2px solid #0033aa;
            border-radius: 8px;
            padding: 12px 18px;
            margin-top: 25px;
            margin-bottom: 8px;
            background: linear-gradient(90deg, rgba(0, 15, 45, 0.5), rgba(0, 5, 20, 0.3));
            animation: neonGlowSoft 5s infinite ease-in-out;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .tabla-titulo {
            color: #66ccff !important;
            font-weight: 700 !important;
            font-size: 18px !important;
            text-shadow: 0 0 8px #0066ff !important;
        }

        /* 3. CONTENEDOR DE PARÁMETROS Y CONFIGURACIÓN */
        .panel-parametros {
            border: 2px solid #0055ff;
            box-shadow: 0 0 15px rgba(0, 120, 255, 0.3);
            border-radius: 10px;
            padding: 20px;
            background-color: rgba(0, 10, 30, 0.4);
            margin-bottom: 25px;
        }

        /* 4. ESTILOS DE TABLAS STREAMLIT */
        [data-testid="stDataFrame"] {
            border: 2px solid #0044aa !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 80, 255, 0.2) !important;
        }

        /* 5. BOTONES MODERNOS Y LLAMATIVOS */
        div.stButton > button {
            width: 100% !important;
            height: 52px !important;
            font-size: 15px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(0, 80, 255, 0.4);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px rgba(0, 180, 255, 0.8);
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


# Función para convertir un DataFrame a Excel en memoria
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
        <h1 class="texto-titulo">⚡ Lector y Traductor de Múltiples Tablas Excel Pro ⚡</h1>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align: center; color: #a0c4ff; font-size: 16px; margin-bottom: 25px;'>"
    "Sube tus archivos de Excel para visualizar, traducir de forma masiva y exportar tus datos con estilo neón dinámico."
    "</p>",
    unsafe_allow_html=True,
)

# Clave dinámica para reiniciar por completo el cargador al borrar
if "uploader_key" not in st.session_state:
  st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "📂 Sube uno o varios archivos Excel (.xlsx)",
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

# === 2. PANEL DE PARÁMETROS (IDIOMAS Y BOTONES) ===
if st.session_state.tablas_originales:
  st.markdown(
      """
        <div class="panel-parametros">
            <h3 style="color: #66ccff; margin-top: 0; text-shadow: 0 0 6px #0044ff;">⚙️ Panel de Parámetros y Configuración</h3>
        """,
      unsafe_allow_html=True,
  )

  idioma_seleccionado = st.selectbox(
      "🌐 ¿A qué idioma deseas traducir la información de las tablas?",
      ("Español (desde inglés)", "Inglés (desde español)"),
      index=0,
  )

  st.write("")
  col1, col2 = st.columns(2)

  with col1:
    btn_traducir = st.button("🚀 PROCESAR Y TRADUCIR TABLAS", type="primary")

  with col2:
    btn_borrar = st.button("🧹 BORRAR Y LIMPIAR PANTALLA", type="secondary")

  st.markdown("</div>", unsafe_allow_html=True)

  # Lógica del botón Traducir
  if btn_traducir:
    target_lang = "es" if "Español" in idioma_seleccionado else "en"

    with st.spinner(
        "🔄 Conectando con el motor de traducción y procesando celdas..."
    ):
      try:
        # Se inicializa el traductor correctamente especificando origen y destino
        source_lang = "en" if target_lang == "es" else "es"
        translator = GoogleTranslator(source=source_lang, target=target_lang)

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

        for (
            nombre_archivo,
            df_orig,
        ) in st.session_state.tablas_originales.items():
          df_traducido = df_orig.copy()

          # Traducir los encabezados de las columnas
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

          # Traducir todas las celdas del DataFrame
          for col in df_traducido.columns:
            df_traducido[col] = (
                df_traducido[col].astype(object).apply(traducir_seguro)
            )

          st.session_state.tablas_render[nombre_archivo] = df_traducido

        st.session_state.idioma_actual = (
            "Traducido al Español"
            if target_lang == "es"
            else "Traducido al Inglés"
        )
        st.success("¡Traducción completada con éxito!")
        st.rerun()
      except Exception as ex:
        st.error(
            f"Hubo un inconveniente con el servicio de traducción: {ex}. Por"
            " favor intenta nuevamente."
        )

  # Lógica del botón Borrar
  if btn_borrar:
    st.session_state.tablas_originales = {}
    st.session_state.tablas_render = {}
    st.session_state.idioma_actual = "Original"
    st.session_state.uploader_key += 1
    st.rerun()

  # === 3. VISTA EN PANTALLA Y DESCARGAS ===
  st.markdown("---")
  st.markdown(
      f"<h4 style='color: #88eeff;'>📊 Estado actual de visualización: <span style='color: #ffffff;'>{st.session_state.idioma_actual}</span></h4>",
      unsafe_allow_html=True,
  )

  for indice, (nombre_archivo, df_tabla) in enumerate(
      st.session_state.tablas_render.items()
  ):
    st.markdown(
        f"""
        <div class="tabla-contenedor">
            <span class="tabla-titulo">📁 Tabla {indice + 1}: {nombre_archivo}</span>
            <span style="color: #00ffcc; font-size: 13px; font-weight: bold;">[ {df_tabla.shape[0]} filas x {df_tabla.shape[1]} columnas ]</span>
        </div>""",
        unsafe_allow_html=True,
    )

    st.dataframe(df_tabla, use_container_width=True)

    # Botón de descarga individual optimizado
    excel_data = convertir_df_a_excel(df_tabla)
    nombre_salida = f"traducido_{nombre_archivo}"

    st.download_button(
        label=f"📥 Descargar '{nombre_archivo}' procesado en Excel",
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
  st.info("💡 Por favor, sube uno o varios archivos Excel para comenzar.")
