import streamlit as st
import pandas as pd
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# --- ESTILO DE ALTO CONTRASTE (SyncData Dark Mode) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Títulos y textos generales */
    h1, h2, h3, p, span {
        color: #FFFFFF !important;
    }

    /* Tarjetas de Métricas (Más oscuras y con borde resaltado) */
    div[data-testid="stMetric"] {
        background-color: #1E2130;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3E44FE; /* Azul SyncData */
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Ajuste de color dentro de las métricas */
    div[data-testid="stMetricLabel"] > div {
        color: #B0BCCB !important; /* Etiqueta en gris claro */
    }
    div[data-testid="stMetricValue"] > div {
        color: #FFD700 !important; /* Valores en Dorado para que resalten */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EN SESIÓN ---
if 'db_mantenimiento' not in st.session_state:
    st.session_state.db_mantenimiento = pd.DataFrame(
        columns=["Fecha", "Local", "Descripción", "Categoría", "Monto (S/)"]
    )

st.title("🛠️ Caja Chica Carlos Ortiz")
st.markdown("<h3 style='color: #3E44FE;'>SyncData - Automatización de datos</h3>", unsafe_allow_html=True)

# --- PANEL LATERAL ---
st.sidebar.header("🔐 Acceso Admin")
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
                st.session_state.db_mantenimiento = pd.concat(
                    [st.session_state.db_mantenimiento, nueva_fila], 
                    ignore_index=True
                )
                st.rerun()
            else:
                st.sidebar.error("Completa todos los campos")

# --- PANEL PRINCIPAL ---
df = st.session_state.db_mantenimiento

# Métricas con colores de alto contraste
col1, col2, col3 = st.columns(3)
total = df["Monto (S/)"].sum()

col1.metric("Gasto Total", f"S/ {total:,.2f}")
col2.metric("N° de Registros", len(df))
col3.metric("Estado", "Activo")

st.write("---")
st.subheader("📋 Historial de Movimientos")

if not df.empty:
    # La tabla de Streamlit se adapta automáticamente al modo oscuro
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Respaldo (CSV)",
        data=csv,
        file_name=f"Caja_Mantenimiento_{date.today()}.csv",
        mime="text/csv",
    )
else:
    st.warning("No hay datos en la sesión actual.")

st.write("---")
st.caption("Desarrollado para Mantenimiento Carlos Ortiz | SyncData 2026")
