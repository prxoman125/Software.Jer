import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Lector y Traductor de Excel", layout="wide")

# Inicializar las variables de estado (Session State)
if "df" not in st.session_state:
    st.session_state.df = None
if "df_original" not in st.session_state:
    st.session_state.df_original = None

# Función para asegurar que los nombres de las columnas sean únicos
def hacer_columnas_unicas(df):
    cols = []
    count = {}
    for col in df.columns:
        col_str = str(col)  # Asegurar que sea texto
        if col_str in count:
            count[col_str] += 1
            cols.append(f"{col_str}_{count[col_str]}")
        else:
            count[col_str] = 0
            cols.append(col_str)
    df.columns = cols
    return df

st.title("📊 Lector y Traductor de Tablas Excel")
st.write("Sube tu archivo de Excel para visualizarlo, modificar el idioma y gestionar los datos.")

# === 1. Cargar archivo Excel ===
uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None and st.session_state.df is None:
    # Leer el archivo Excel
    try:
        df_leido = pd.read_excel(uploaded_file)
        # Asegurar columnas únicas desde la carga inicial
        st.session_state.df = hacer_columnas_unicas(df_leido)
        st.session_state.df_original = st.session_state.df.copy()
        st.success("¡Archivo cargado con éxito!")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# === 2. Funciones y Botones de Interfaz ===
if st.session_state.df is not None:
    
    # SOLUCIÓN: Especificamos explícitamente el número 2 para generar dos columnas
    col1, col2 = st.columns(2)

    with col1:
        # Selector de idioma
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir:",
            ("Español (de inglés)", "Inglés (de español)"),
            index=0
        )

    with col2:
        st.write("")
        st.write("")
        # Botón para borrar tablas
        if st.button("🗑️ Borrar Tabla", type="primary"):
            st.session_state.df = None
            st.session_state.df_original = None
            st.rerun()

    # === 3. Lógica de Traducción ===
    if st.session_state.df is not None:
        if idioma_seleccionado == "Español (de inglés)":
            target_lang = "es"
        else:
            target_lang = "en"

        if st.button("Traducir Tabla"):
            with st.spinner("Traduciendo el contenido, por favor espera..."):
                translator = GoogleTranslator(source='auto', target=target_lang)
                
                def traducir_valor(val):
                    if isinstance(val, str) and val.strip():
                        return translator.translate(val)
                    return val

                # Traducir los encabezados originales
                df_traducido = st.session_state.df_original.copy()
                nuevas_columnas = []
                for col in df_traducido.columns:
                    try:
                        nuevas_columnas.append(translator.translate(str(col)))
                    except:
                        nuevas_columnas.append(str(col))
                
                df_traducido.columns = nuevas_columnas
                
                # Forzar que sigan siendo únicas después de la traducción
                df_traducido = hacer_columnas_unicas(df_traducido)
                
                # Traducir las celdas de la tabla
                for col in df_traducido.columns:
                    df_traducido[col] = df_traducido[col].apply(traducir_valor)

                st.session_state.df = df_traducido
                st.success("¡Traducción completada!")

    # === 4. Mostrar la tabla ===
    st.write("### Vista previa de los datos:")
    st.dataframe(st.session_state.df, use_container_width=True)

else:
    st.info("Por favor, sube un archivo Excel para comenzar.")
