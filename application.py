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

st.title("📊 Lector y Traductor de Tablas Excel")
st.write("Sube tu archivo de Excel para visualizarlo, modificar el idioma y gestionar los datos.")

# === 1. Cargar archivo Excel ===
uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        st.session_state.df = pd.read_excel(uploaded_file)
        # Guardamos una copia exacta para poder revertir o retraducir
        st.session_state.df_original = st.session_state.df.copy()
        st.success("¡Archivo cargado con éxito!")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# === 2. Funciones y Botones de Interfaz ===
if st.session_state.df is not None:
    
    # Crear dos columnas para el selector de idioma y el botón de borrar
    col1, col2 = st.columns([4, 1])

    with col1:
        # Selector de idioma
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir:",
            ("Español (de inglés)", "Inglés (de español)"),
            index=0
        )

    with col2:
        # Espacio en blanco para alinear
        st.write("")
        st.write("")
        # Botón para borrar tablas
        if st.button("🗑️ Borrar Tabla", type="primary"):
            st.session_state.df = None
            st.session_state.df_original = None
            st.rerun()  # Recarga la app para limpiar la pantalla

    # === 3. Lógica de Traducción ===
    if st.session_state.df is not None:
        if idioma_seleccionado == "Español (de inglés)":
            target_lang = "es"
        else:
            target_lang = "en"

        if st.button("Traducir Tabla"):
            with st.spinner("Traduciendo el contenido, por favor espera..."):
                # Instanciamos el traductor
                translator = GoogleTranslator(source='auto', target=target_lang)
                
                # Función para traducir elementos (manejando nulos/números)
                def traducir_valor(val):
                    if isinstance(val, str):
                        return translator.translate(val)
                    return val

                # Aplicamos la traducción a los encabezados y a todas las celdas
                df_traducido = st.session_state.df_original.copy()
                df_traducido.columns = [translator.translate(col) for col in df_traducido.columns]
                
                for col in df_traducido.columns:
                    df_traducido[col] = df_traducido[col].apply(traducir_valor)

                # Guardamos el df traducido en el estado
                st.session_state.df = df_traducido
                st.success("¡Traducción completada!")

    # === 4. Mostrar la tabla ===
    st.write("### Vista previa de los datos:")
    st.dataframe(st.session_state.df, use_container_width=True)

else:
    st.info("Por favor, sube un archivo Excel para comenzar.")
