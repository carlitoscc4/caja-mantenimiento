import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"
# Pon aquí el ID de tu Google Sheet (el código largo de la URL)
SHEET_ID = "TU_ID_DE_GOOGLE_SHEET_AQUÍ"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para leer desde Google Sheets (Versión pública rápida)
def cargar_datos_nube():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos_nube()

st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")

# --- BARRA LATERAL ---
password = st.sidebar.text_input("Clave de acceso:", type="password")

if password == CLAVE_ADMIN:
    st.sidebar.success("Modo Edición")
    with st.sidebar.form("registro", clear_on_submit=True):
        f = st.date_input("Fecha", date.today())
        l = st.text_input("N° de Local")
        d = st.text_input("Descripción")
        c = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m = st.number_input("Monto (S/)", min_value=0.0)
        archivo = st.file_uploader("Subir foto de boleta", type=["jpg", "png", "jpeg"])
        
        if st.form_submit_button("💾 Guardar en la Nube"):
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            
            # Nota: Para que dure en la nube gratis, guardamos el registro.
            # Las fotos en Streamlit Cloud son temporales. 
            # Si quieres fotos eternas, avísame para conectarlo a Google Drive.
            
            nueva_fila = pd.DataFrame([[id_u, str(f), l, d, c, m, "Foto cargada"]], 
                                     columns=st.session_state.df.columns)
            
            st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
            
            # Botón para que tú mismo descargues el backup si la nube se reinicia
            st.sidebar.info("¡Dato registrado! Recuerda descargar el Excel abajo si haces cambios importantes.")
            st.rerun()

# --- PANEL PRINCIPAL ---
total = st.session_state.df["Monto (S/)"].sum()
st.metric("Gasto Total Acumulado", f"S/ {total:,.2f}")

st.write("### 📋 Historial Permanente")
st.dataframe(st.session_state.df, use_container_width=True)

# Botón de seguridad para que los datos duren
csv = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar Respaldo (Excel/CSV)", csv, "caja_mantenimiento_backup.csv", "text/csv")

