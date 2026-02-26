import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

# URL de respuesta de tu formulario de Google
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd92A98fvp-Eae8-wKGDoCwxRKjjkZyFOEVZzywBTb31mAQYQ/formResponse"

# ID de tu hoja de cálculo de Google
SHEET_ID = "1ORuU56oKeW7Y6pNgj--gX_-AYDxQAiZZFYnYEGBK-d8"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para LEER los datos del Excel
def cargar_datos_nube():
    # Se apunta al GID 1791632682 que es donde están tus respuestas según tu enlace
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1791632682"
    try:
        df = pd.read_csv(url)
        # Limpiamos filas que Google a veces entrega vacías
        df = df.dropna(subset=['Local', 'Descripción'], how='all')
        return df
    except:
        # Si falla la lectura, devolvemos un cuadro vacío con la estructura correcta
        return pd.DataFrame(columns=["Marca temporal", "ID", "Fecha", "Local", "Descripción", "Categoría", "Monto"])

# Inicializar los datos en la sesión
if 'df' not in st.session_state:
    st.session_state.df = cargar_

