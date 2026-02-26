import streamlit as st
import pandas as pd
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Estilo personalizado para SyncData
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS EN LA NUBE (Memoria temporal) ---
if 'db_mantenimiento' not in st.session_state:
    # Creamos una tabla vacía con las columnas que necesitas
    st.session_state.db_mantenimiento = pd.DataFrame(
        columns=["Fecha", "Local", "Descripción", "Categoría", "Monto (S/)"]
    )

st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")
st.info("Slogan: SyncData - Automatización de datos")

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
            # Creamos la nueva fila
            nueva_fila = pd.DataFrame({
                "Fecha": [str(fecha_gasto)],
                "Local": [n_local],
                "Descripción": [desc],
                "Categoría": [cat],
                "Monto (S/)": [monto]
            })
            
            # La añadimos a la base de datos en memoria
            st.session_state.db_mantenimiento = pd.concat(
                [st.session_state.df_mantenimiento if 'df_mantenimiento' in locals() else st.session_state.db_mantenimiento, nueva_fila], 
                ignore_index=True
            )
            st.sidebar.balloons()
            st.rerun()

# --- PANEL PRINCIPAL ---
df = st.session_state.db_mantenimiento

# Métricas rápidas
col1, col2, col3 = st.columns(3)
total = df["Monto (S/)"].sum()
registros = len(df)

col1.metric("Gasto Total", f"S/ {total:,.2f}")
col2.metric("N° de Registros", registros)
col3.metric("Empresa", "SyncData")

st.write("---")
st.subheader("📋 Historial de Movimientos")

if not df.empty:
    # Mostramos la tabla interactiva
    st.dataframe(df, use_container_width=True)
    
    # BOTÓN DE ORO: Descargar para que los datos duren
    st.write("⚠️ **Importante:** Para que tus datos duren para siempre, descarga tu respaldo al finalizar el día:")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Excel de Respaldo (CSV)",
        data=csv,
        file_name=f"Caja_Mantenimiento_{date.today()}.csv",
        mime="text/csv",
    )
else:
    st.warning("Aún no hay datos registrados en esta sesión.")

st.write("---")
st.caption("Desarrollado para Mantenimiento Carlos Ortiz | SyncData 2026")



