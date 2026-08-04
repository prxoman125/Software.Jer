import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Lector y Traductor Multitabla", layout="wide")

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
st.write("Sube todos los archivos que quieras. Se mostrarán uno debajo del otro y se traducirán al presionar el botón.")

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
    # Verificamos si hay archivos nuevos que no hemos procesado aún
    archivos_actuales = [f.name for f in uploaded_files]
    
    # SOLUCIÓN: Convertimos las llaves a lista explícitamente para evitar el AttributeError
    llaves_guardadas = list(st.session_state.tablas_originales.keys())
    
    if set(archivos_actuales) != set(llaves_guardadas):
        nuevos_originales = {}
        nuevos_render = {}
        
        for file in uploaded_files:
            # Si ya lo teníamos cargado, conservamos lo que había
            if file.name in st.session_state.tablas_originales:
                nuevos_originales[file.name] = st.session_state.tablas_originales[file.name]
                nuevos_render[file.name] = st.session_state.tablas_render[file.name]
            else:
                # Si es un archivo nuevo, lo leemos por primera vez
                try:
                    df = pd.read_excel(file)
                    df = hacer_columnas_unicas(df)
                    nuevos_originales[file.name] = df.copy()
                    nuevos_render[file.name] = df.copy() # Al inicio es igual al original
                except Exception as e:
                    st.error(f"Error al leer el archivo {file.name}: {e}")
        
        st.session_state.tablas_originales = nuevos_originales
        st.session_state.tablas_render = nuevos_render
        # Si el usuario cambia los archivos, regresamos el estado visual al modo original
        st.session_state.idioma_actual = "Original"

# === 2. PANEL DE INTERFAZ (IDIOMAS Y BORRADO) ===
if st.session_state.tablas_originales:
    col1, col2 = st.columns(2)

    with col1:
        idioma_seleccionado = st.selectbox(
            "Selecciona el idioma al que deseas traducir:",
            ("Español (de inglés)", "Inglés (de español)"),
            index=0
        )
        
        # Botón de traducción masiva
        if st.button("🔄 Traducir Todas las Tablas", type="secondary"):
            target_lang = "es" if idioma_seleccionado == "Español (de inglés)" else "en"
            
            with st.spinner("Traduciendo celdas y encabezados, por favor espera..."):
                translator = GoogleTranslator(source='auto', target=target_lang)
                
                def traducir_valor(val):
                    if isinstance(val, str) and val.strip():
                        return translator.translate(val)
                    return val

                # Traducimos a partir de los datos limpios almacenados en 'tablas_originales'
                for nombre_archivo, df_orig in st.session_state.tablas_originales.items():
                    df_traducido = df_orig.copy()
                    
                    # Traducir los encabezados
                    nuevas_cols = []
                    for col in df_traducido.columns:
                        try:
                            nuevas_cols.append(translator.translate(str(col)))
                        except:
                            nuevas_cols.append(str(col))
                    df_traducido.columns = nuevas_cols
                    df_traducido = hacer_columnas_unicas(df_traducido)
                    
                    # Traducir los valores de las celdas
                    for col in df_traducido.columns:
                        df_traducido[col] = df_traducido[col].apply(traducir_valor)
                    
                    # Guardamos la tabla ya traducida en la variable de renderizado
                    st.session_state.tablas_render[nombre_archivo] = df_traducido
                
                st.session_state.idioma_actual = "Traducido"
                st.success("¡Todas las tablas fueron traducidas con éxito!")
                st.rerun() # Forzar actualización inmediata de la interfaz

    with col2:
        st.write("")
        st.write("")
        # Botón para borrar todo
        if st.button("🗑️ Borrar Todas las Tablas", type="primary"):
            st.session_state.tablas_originales = {}
            st.session_state.tablas_render = {}
            st.session_state.idioma_actual = "Original"
            st.session_state.uploader_key += 1 
            st.rerun()

    # === 3. VISTA EN PANTALLA ===
    st.write("---")
    st.write(f"### Visualizando tablas en modo: **{st.session_state.idioma_actual}**")
    
    # Recorremos la memoria interna de renderizado de forma ordenada hacia abajo
    for indice, (nombre_archivo, df_tabla) in enumerate(st.session_state.tablas_render.items()):
        st.markdown(f"#### 📄 Tabla {indice + 1}: `{nombre_archivo}`")
        st.dataframe(df_tabla, use_container_width=True)
        st.write("") 

else:
    # Limpieza automática si se remueven manualmente los archivos de la caja
    if not uploaded_files and st.session_state.tablas_originales:
        st.session_state.tablas_originales = {}
        st.session_state.tablas_render = {}
        st.session_state.idioma_actual = "Original"
        st.rerun()
    st.info("Por favor, sube uno o varios archivos Excel para comenzar.")
