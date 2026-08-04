import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Lector y Traductor Multitabla", layout="wide")

# Inicializar las variables de estado para recordar las traducciones
if "tablas_traducidas" not in st.session_state:
    st.session_state.tablas_traducidas = {}
if "idioma_actual" not in st.session_state:
    st.session_state.idioma_actual = "Original"

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
st.write("Sube todos los archivos que quieras. Se mostrarán uno debajo del otro.")

# === 1. Selector de Archivos Múltiples ===
# Usamos una clave (key) para poder resetear el componente con el botón de borrar
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "Sube uno o varios archivos Excel (.xlsx)", 
    type=["xlsx"], 
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

# === 2. Panel de Control (Idiomas y Borrado) ===
if uploaded_files:
    col1, col2 = st.columns(2)

    with col1:
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir:",
            ("Español (de inglés)", "Inglés (de español)"),
            index=0
        )
        
        # Botón para ejecutar la traducción
        if st.button("🔄 Traducir Todas las Tablas", type="secondary"):
            target_lang = "es" if idioma_seleccionado == "Español (de inglés)" else "en"
            
            with st.spinner("Traduciendo todas las tablas en pantalla..."):
                translator = GoogleTranslator(source='auto', target=target_lang)
                
                def traducir_valor(val):
                    if isinstance(val, str) and val.strip():
                        return translator.translate(val)
                    return val

                # Procesamos cada archivo que está subido actualmente
                for file in uploaded_files:
                    try:
                        # Leer archivo original
                        df = pd.read_excel(file)
                        df = hacer_columnas_unicas(df)
                        
                        # Traducir encabezados
                        nuevas_cols = []
                        for col in df.columns:
                            try:
                                nuevas_cols.append(translator.translate(str(col)))
                            except:
                                nuevas_cols.append(str(col))
                        df.columns = nuevas_cols
                        df = hacer_columnas_unicas(df)
                        
                        # Traducir celdas
                        for col in df.columns:
                            df[col] = df[col].apply(traducir_valor)
                        
                        # Guardar resultado en el estado usando el nombre del archivo como clave
                        st.session_state.tablas_traducidas[file.name] = df
                    except Exception as e:
                        st.error(f"Error al traducir {file.name}: {e}")
                
                st.session_state.idioma_actual = "Traducido"
                st.success("¡Traducción completada con éxito!")

    with col2:
        st.write("")
        st.write("")
        # Botón para borrar todo y limpiar la pantalla por completo
        if st.button("🗑️ Borrar Todas las Tablas", type="primary"):
            st.session_state.tablas_traducidas = {}
            st.session_state.idioma_actual = "Original"
            st.session_state.uploader_key += 1  # Cambia la clave para forzar la limpieza del uploader
            st.rerun()

    # === 3. Renderizado de las Tablas en Pantalla ===
    st.write("---")
    st.write(f"### Visualizando tablas en modo: **{st.session_state.idioma_actual}**")
    
    # Este ciclo recorre TODOS los archivos cargados en tiempo real y los dibuja uno abajo del otro
    for indice, file in enumerate(uploaded_files):
        with st.container():
            st.markdown(f"#### 📄 Tabla {indice + 1}: `{file.name}`")
            
            try:
                # Si ya fue traducido y está guardado en memoria, muestra la traducción
                if st.session_state.idioma_actual == "Traducido" and file.name in st.session_state.tablas_traducidas:
                    df_a_mostrar = st.session_state.tablas_traducidas[file.name]
                else:
                    # Si no, lee y muestra el archivo original inmediatamente
                    df_a_mostrar = pd.read_excel(file)
                    df_a_mostrar = hacer_columnas_unicas(df_a_mostrar)
                
                # Renderiza la tabla en la pantalla
                st.dataframe(df_a_mostrar, use_container_width=True)
                st.write("")  # Espacio de separación entre tablas
                
            except Exception as e:
                st.error(f"No se pudo mostrar el archivo {file.name}: {e}")

else:
    # Si no hay archivos, aseguramos que la memoria esté limpia
    st.session_state.tablas_traducidas = {}
    st.session_state.idioma_actual = "Original"
    st.info("Por favor, sube uno o varios archivos Excel para comenzar.")
