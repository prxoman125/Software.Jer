import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from requests import Session

# ==========================================
# PARCHE DE SEGURIDAD CONTRA ERROR 500 GOOGLE
# ==========================================
_original_send = Session.send
def _patched_send(*args, **kwargs):
    request = args
    request.headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    return _original_send(*args, **kwargs)
Session.send = _patched_send
# ==========================================

# Configuración de la página
st.set_page_config(page_title="Lector y Traductor Multitabla", layout="wide")

# ==========================================
# DISEÑO PERSONALIZADO: AZUL OSCURO NEÓN (SIN EMOJIS)
# ==========================================
st.markdown("""
    <style>
        /* Estilo neón azul oscuro para los contenedores de las tablas */
        .tabla-contenedor {
            border: 2px solid #0055ff !important;
            box-shadow: 0 0 10px #0022aa, inset 0 0 5px #001155 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            margin-bottom: 25px !important;
            background-color: transparent !important;
        }
        /* Estilo para los títulos de cada tabla */
        .tabla-titulo {
            color: #0088ff !important;
            font-weight: bold !important;
            text-shadow: 0 0 5px #0033aa !important;
            margin-bottom: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

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

st.title("Lector y Traductor de Multiples Tablas Excel")
st.write("Sube tus archivos. El sistema cuenta con parches automatizados contra caidas de servidor.")

# Clave dinámica para reiniciar por completo el cargador al borrar
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "Sube uno o varios archivos Excel (.xlsx)", 
    type=["xlsx"], 
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
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
                nuevos_originales[file.name] = st.session_state.tablas_originales[file.name]
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

# === 2. PANEL DE INTERFAZ (IDIOMAS Y BORRADO) ===
if st.session_state.tablas_originales:
    col1, col2 = st.columns(2)

    with col1:
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir:",
            ("Español (de ingles)", "Ingles (de espanol)"),
            index=0
        )
        
        if st.button("Traducir Todas las Tablas", type="secondary"):
            target_lang = "es" if idioma_seleccionado == "Español (de ingles)" else "en"
            
            with st.spinner("Traduciendo registros... Por favor espera..."):
                try:
                    translator = GoogleTranslator(source='auto', target=target_lang)
                    
                    def traducir_seguro(val):
                        if pd.isna(val): 
                            return val
                        val_str = str(val).strip()
                        if val_str and not val_str.replace('.', '', 1).isdigit():
                            try:
                                return translator.translate(val_str)
                            except:
                                return val
                        return val

                    for nombre_archivo, df_orig in st.session_state.tablas_originales.items():
                        df_traducido = df_orig.copy()
                        
                        nuevas_cols = []
                        for col in df_traducido.columns:
                            col_str = str(col).strip()
                            if col_str and not col_str.isdigit():
                                try:
                                    nuevas_cols.append(translator.translate(col_str))
                                except:
                                    nuevas_cols.append(col_str)
                            else:
                                nuevas_cols.append(col_str)
                                
                        df_traducido.columns = nuevas_cols
                        df_traducido = hacer_columnas_unicas(df_traducido)
                        
                        for col in df_traducido.columns:
                            df_traducido[col] = df_traducido[col].apply(traducir_seguro)
                        
                        st.session_state.tablas_render[nombre_archivo] = df_traducido
                    
                    st.session_state.idioma_actual = "Traducido"
                    st.success("Todas las tablas fueron traducidas con exito")
                    st.rerun()
                except Exception as error_global:
                    st.error(f"Error de conexion con el servidor de traduccion. Por favor intenta de nuevo.")

    with col2:
        st.write("")
        st.write("")
        if st.button("Borrar Todas las Tablas", type="primary"):
            st.session_state.tablas_originales = {}
            st.session_state.tablas_render = {}
            st.session_state.idioma_actual = "Original"
            st.session_state.uploader_key += 1 
            st.rerun()

    # === 3. VISTA EN PANTALLA ===
    st.write("---")
    st.write(f"Visualizando tablas en modo: **{st.session_state.idioma_actual}**")
    
    # Renderizado con contenedores HTML para aplicar los bordes azul neón oscuros
    for indice, (nombre_archivo, df_tabla) in enumerate(st.session_state.tablas_render.items()):
        st.markdown(f"""
            <div class="tabla-contenedor">
                <div class="tabla-titulo">Tabla {indice + 1}: {nombre_archivo}</div>
            </div>
        """, unsafe_allow_html=True)
        # La tabla se coloca justo debajo del contenedor con borde neón
        st.dataframe(df_tabla, use_container_width=True)
        st.write("") 

else:
    if not uploaded_files and st.session_state.tablas_originales:
        st.session_state.tablas_originales = {}
        st.session_state.tablas_render = {}
        st.session_state.idioma_actual = "Original"
        st.rerun()
    st.info("Por favor, sube uno o varios archivos Excel para comenzar.")
