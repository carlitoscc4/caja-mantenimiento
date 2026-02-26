import streamlit as st
import pandas as pd
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

st.set_page_config(page_title="Ortiz Mantenimiento", layout="wide", page_icon="🛠️")

# --- ESTILO DE ALTO CONTRASTE (Oscuro y Profesional) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Títulos y textos generales */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* Tarjetas de Métricas */
    div[data-testid="stMetric"] {
        background-color: #1E2130;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3E44FE;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Ajuste de color dentro de las métricas */
    div[data-testid="stMetricLabel"] > div {
        color: #B0BCCB !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #FFD700 !important; /* Dorado para los montos */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
    
    /* Estilo del pie de página */
    .footer {
        text-align: center;
        padding: 20px;
        color: #888888;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EN SESIÓN ---
if 'db_mantenimiento' not in st.session_state:
    st.session_state.db_mantenimiento = pd.DataFrame(
        columns=["Fecha", "Local", "Descripción", "Categoría", "Monto (S/)"]
    )

st.title("🛠️ Caja Chica - Ortiz Mantenimiento")
st.markdown("<p style='color: #3E44FE; font-weight: bold;'>Sistema de Control de Gastos | SyncData</p>", unsafe_allow_html=True)

# --- PANEL LATERAL ---
st.sidebar.header("🔐 Acceso Administrativo")
password = st.sidebar.text_input("Ingresa la clave:", type="password")

if password == CLAVE_ADMIN:
    st.sidebar.success("Modo Edición Activado")
    
    with st.sidebar.form("formulario_registro", clear_on_submit=True):
        st.subheader("📝 Registrar Gasto")
        fecha_gasto = st.date_input("Fecha", date.today())
        n_local = st.text_input("N° de Local")
        desc = st.text_input("Descripción")
        cat = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Materiales", "Otros"])
        monto = st.number_input("Monto (S/)", min_value=0.0, step=0.50)
        
        if st.form_submit_button("💾 Guardar Registro"):
            if n_local and desc and monto > 0:
                nueva_fila = pd.DataFrame({
                    "Fecha": [str(fecha_gasto)],
                    "Local": [n_local],
                    "Descripción": [desc],
                    "Categoría": [cat],
                    "Monto (S/)": [monto]
                })
                # Concatenación segura
                st.session_state.db_mantenimiento = pd.concat(
                    [st.session_state.db_mantenimiento, nueva_fila], 
                    ignore_index=True
                )
                st.sidebar.balloons()
                st.rerun()
            else:
                st.sidebar.error("Por favor, completa todos los campos.")

# --- PANEL PRINCIPAL ---
df = st.session_state.db_mantenimiento

# Métricas
col1, col2, col3 = st.columns(3)
total = df["Monto (S/)"].sum()

col1.metric("Gasto Total", f"S/ {total:,.2f}")
col2.metric("Registros", len(df))
