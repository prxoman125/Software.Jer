import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Lector y Traductor Multitabla", layout="wide")

# Inicializar las variables de estado (Session State)
# Ahora guardamos listas de DataFrames para manejar múltiples archivos
if "tablas" not in st.session_state:
    st.session_state.tablas = []
if "tablas_originales" not in st.session_state:
    st.session_state.tablas_originales = []

# Función para asegurar que los nombres de las columnas sean únicos
def hacer_columnas_unicas(df):
    cols = []
    count = {}
    for col in df.columns:
        col_str = str(col)
        if col_str in count:
            count[col_str] += 1
            cols.append(f"{col_str}_{count[col_str]}")
        else:
            count[col_str] = 0
            cols.append(col_str)
    df.columns = cols
    return df

st.title("📊 Lector y Traductor de Múltiples Tablas Excel")
st.write("Sube uno o varios archivos de Excel para visualizarlos todos abajo, traducirlos o gestionarlos en conjunto.")

# === 1. Cargar múltiples archivos Excel ===
# SOLUCIÓN: Agregamos accept_multiple_files=True
uploaded_files = st.file_uploader(
    "Sube uno o varios archivos Excel (.xlsx)", 
    type=["xlsx"], 
    accept_multiple_files=True
)

# Lógica para procesar los archivos cargados
if uploaded_files:
    # Si la lista en sesión está vacía, cargamos los archivos
    if not st.session_state.tablas:
        tablas_cargadas = []
        nombres_archivos = []
        for file in uploaded_files:
            try:
                df_leido = pd.read_excel(file)
                df_unico = hacer_columnas_unicas(df_leido)
                # Guardamos el DataFrame junto con el nombre del archivo para identificarlo
                tablas_cargadas.append({"nombre": file.name, "df": df_unico})
            except Exception as e:
                st.error(f"Error al leer el archivo {file.name}: {e}")
        
        if tablas_cargadas:
            st.session_state.tablas = tablas_cargadas
            # Creamos una copia profunda para los originales
            st.session_state.tablas_originales = [
                {"nombre": t["nombre"], "df": t["df"].copy()} for t in tablas_cargadas
            ]
            st.success(f"¡Se han cargado {len(tablas_cargadas)} archivo(s) con éxito!")

# === 2. Funciones y Botones de Interfaz ===
if st.session_state.tablas:
    
    col1, col2 = st.columns(2)

    with col1:
        # Selector de idioma
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir todas las tablas:",
            ("Español (de inglés)", "Inglés (de español)"),
            index=0
        )

    with col2:
        st.write("")
        st.write("")
        # Botón para borrar TODAS las tablas de la pantalla
        if st.button("🗑️ Borrar Todas las Tablas", type="primary"):
            st.session_state.tablas = []
            st.session_state.tablas_originales = []
            st.rerun()

    # === 3. Lógica de Traducción Multitabla ===
    if st.session_state.tablas:
        target_lang = "es" if idioma_seleccionado == "Español (de inglés)" else "en"

        if st.button("Traducir Todas las Tablas"):
            with st.spinner("Traduciendo todo el contenido, por favor espera..."):
                translator = GoogleTranslator(source='auto', target=target_lang)
                
                def traducir_valor(val):
                    if isinstance(val, str) and val.strip():
                        return translator.translate(val)
                    return val

                nuevas_tablas = []
                
                # Iteramos y traducimos cada tabla guardada
                for t_orig in st.session_state.tablas_originales:
                    df_traducido = t_orig["df"].copy()
                    
                    # 1. Traducir encabezados
                    nuevas_columnas = []
                    for col in df_traducido.columns:
                        try:
                            nuevas_columnas.append(translator.translate(str(col)))
                        except:
                            nuevas_columnas.append(str(col))
                    df_traducido.columns = nuevas_columnas
                    df_traducido = hacer_columnas_unicas(df_traducido)
                    
                    # 2. Traducir celdas
                    for col in df_traducido.columns:
                        df_traducido[col] = df_traducido[col].apply(traducir_valor)
                    
                    nuevas_tablas.append({"nombre": t_orig["nombre"], "df": df_traducido})
                
                st.session_state.tablas = nuevas_tablas
                st.success("¡Traducción de todas las tablas completada!")

    # === 4. Mostrar todas las tablas una debajo de otra ===
    st.write("---")
    st.write("### Vista previa de las tablas cargadas:")
    
    for indice, elemento in enumerate(st.session_state.tablas):
        # Usamos un contenedor expandible para que la interfaz se vea ordenada
        with st.expander(f"📄 Archivo {indice + 1}: {elemento['nombre']}", expanded=True):
            st.dataframe(elemento["df"], use_container_width=True)

else:
    # Si el usuario quitó los archivos del cargador, limpiamos la pantalla
    if not uploaded_files and (st.session_state.tablas):
        st.session_state.tablas = []
        st.session_state.tablas_originales = []
        st.rerun()
    st.info("Por favor, sube uno o varios archivos Excel para comenzar.")
