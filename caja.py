import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

# URL de respuesta de tu formulario de Google
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd92A98fvp-Eae8-wKGDoCwxRKjjkZyFOEVZzywBTb31mAQYQ/formResponse"

# ID de tu hoja de cálculo (Extraído de tu enlace)
SHEET_ID = "1ORuU56oKeW7Y6pNgj--gX_-AYDxQAiZZFYnYEGBK-d8"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para LEER los datos del Excel
def cargar_datos_nube():
    # Apuntamos directamente a la hoja de respuestas (gid=1791632682)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1791632682"
    try:
        df = pd.read_csv(url)
        # Limpiamos filas que no tengan descripción para evitar el error de "None"
        df = df.dropna(subset=['Descripción'], how='all')
        return df
    except:
        return pd.DataFrame(columns=["Marca temporal", "ID", "Fecha", "Local", "Descripción", "Categoría", "Monto"])

# Inicializar los datos en la sesión
if 'df' not in st.session_state:
    st.session_state.df = cargar_datos_nube()

st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")

# --- BARRA LATERAL (Acceso y Registro) ---
st.sidebar.title("🔐 Acceso")
pass_input = st.sidebar.text_input("Clave de administrador:", type="password")

if pass_input == CLAVE_ADMIN:
    st.sidebar.success("✅ Modo Edición Activo")
    with st.sidebar.form("registro", clear_on_submit=True):
        st.header("📝 Nuevo Registro")
        f = st.date_input("Fecha", date.today())
        l = st.text_input("N° de Local")
        d = st.text_input("Descripción del gasto")
        c = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m = st.number_input("Monto (S/)", min_value=0.0, step=0.10)
        
        if st.form_submit_button("💾 Guardar en Google Sheets"):
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            
            # Mapeo de campos entry de tu formulario
            datos_enviar = {
                "entry.1593539825": id_u,
                "entry.122394

