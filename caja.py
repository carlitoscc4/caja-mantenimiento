import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"
# ID de tu hoja (es el código largo que está en la URL entre /d/ y /edit)
SHEET_ID = "PON_AQUI_SOLO_EL_ID_DE_TU_HOJA"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para leer datos (esto sí funciona con URL pública)
def cargar_datos():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])

# Cargamos los datos en la sesión
if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")

# --- SEGURIDAD Y REGISTRO ---
st.sidebar.title("🔐 Acceso")
password = st.sidebar.text_input("Clave:", type="password")

if password == CLAVE_ADMIN:
    st.sidebar.success("Modo Edición")
    with st.sidebar.form("registro", clear_on_submit=True):
        f = st.date_input("Fecha", date.today())
        l = st.text_input("N° de Local")
        d = st.text_input("Descripción")
        c = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m = st.number_input("Monto (S/)", min_value=0.0)
        
        if st.form_submit_button("💾 Guardar"):
            # Aquí va el truco: En lugar de conn.update, simplemente añadimos a la sesión 
            # y te daré un paso extra para que sea permanente.
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            nueva_fila = pd.DataFrame([[id_u, str(f), l, d, c, m, "Sin foto"]], 
                                     columns=st.session_state.df.columns)
            
            st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
            st.success("¡Registrado en la sesión! (Para persistencia total usa Google Forms)")
            st.rerun()

# --- TABLA Y RESUMEN ---
total = st.session_state.df["Monto (S/)"].sum()
st.metric("Gasto Total", f"S/ {total:,.2f}")
st.dataframe(st.session_state.df, use_container_width=True)

# Botón para descargar lo acumulado
csv = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar Backup CSV", csv, "caja_mantenimiento.csv", "text/csv")
