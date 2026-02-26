import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
from datetime import date

# --- CONFIGURACIÓN DE SEGURIDAD Y HOJA ---
CLAVE_ADMIN = "jess7386"
URL_SHEET = "https://docs.google.com/spreadsheets/d/1ORuU56oKeW7Y6pNgj--gX_-AYDxQAiZZFYnYEGBK-d8/edit?gid=0#gid=0"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Conectar con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos():
    try:
        return conn.read(spreadsheet=URL_SHEET, usecols=[0,1,2,3,4,5,6])
    except:
        return pd.DataFrame(columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

# --- SEGURIDAD ---
st.sidebar.title("🔐 Acceso")
password = st.sidebar.text_input("Clave:", type="password")
es_admin = (password == CLAVE_ADMIN)

if es_admin:
    with st.sidebar.form("registro"):
        st.header("📝 Nuevo Registro")
        f = st.date_input("Fecha", date.today())
        l = st.text_input("N° de Local")
        d = st.text_input("Descripción")
        c = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m = st.number_input("Monto (S/)", min_value=0.0)
        
        if st.form_submit_button("💾 Guardar en Google"):
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            # Por ahora guardamos sin foto para asegurar la conexión
            nueva_fila = pd.DataFrame([[id_u, str(f), l, d, c, m, "Sin foto"]], 
                                     columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])
            
            # Actualizar Google Sheets
            actualizado = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=actualizado)
            st.session_state.df = actualizado
            st.success("¡Sincronizado con Google!")
            st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")
st.write(f"### Total: S/ {st.session_state.df['Monto (S/)'].sum():,.2f}")
st.dataframe(st.session_state.df, use_container_width=True)
