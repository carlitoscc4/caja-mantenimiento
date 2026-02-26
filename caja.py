import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CONFIGURACIÓN DE SEGURIDAD ---
CLAVE_ADMIN = "jess7386" 

# Archivos y carpetas
ARCHIVO_DATOS = "datos_caja_chica.csv"
CARPETA_FOTOS = "fotos_boletas"

if not os.path.exists(CARPETA_FOTOS):
    os.makedirs(CARPETA_FOTOS)

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    return pd.DataFrame(columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

# --- SEGURIDAD EN BARRA LATERAL ---
st.sidebar.title("🔐 Acceso Restringido")
password = st.sidebar.text_input("Clave para modificar:", type="password")

es_admin = (password == CLAVE_ADMIN)

if es_admin:
    st.sidebar.success("✅ Modo Edición Activo")
    with st.sidebar.form("formulario_registro", clear_on_submit=True):
        st.header("📝 Nuevo Registro")
        f_reg = st.date_input("Fecha", date.today())
        l_reg = st.text_input("N° de Local")
        d_reg = st.text_input("Descripción")
        c_reg = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m_reg = st.number_input("Monto (S/)", min_value=0.0, step=0.10)
        a_reg = st.file_uploader("Subir boleta (Foto/PDF)", type=["jpg", "png", "jpeg", "pdf"])
        
        if st.form_submit_button("💾 Guardar en Caja"):
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            n_foto = "Sin foto"
            if a_reg:
                n_foto = f"{id_u}_{a_reg.name}"
                with open(os.path.join(CARPETA_FOTOS, n_foto), "wb") as f:
                    f.write(a_reg.getbuffer())
            
            nueva_fila = pd.DataFrame([[id_u, f_reg, l_reg, d_reg, c_reg, m_reg, n_foto]], 
                                     columns=["ID", "Fecha", "N° Local", "Descripción", "Categoría", "Monto (S/)", "Foto"])
            st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
            st.session_state.df.to_csv(ARCHIVO_DATOS, index=False)
            st.rerun()
else:
    st.sidebar.warning("🔒 Ingrese clave para registrar gastos.")

# --- PANEL PRINCIPAL ---
st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")

c1, c2 = st.columns(2)
total_dinero = st.session_state.df["Monto (S/)"].sum()
c1.metric("Gasto Total Acumulado", f"S/ {total_dinero:,.2f}")
c2.metric("N° de Registros", len(st.session_state.df))

st.write("---")
st.write("### 📋 Historial de Movimientos")
st.dataframe(st.session_state.df.drop(columns=["ID"]), use_container_width=True)

# Visor de fotos
if not st.session_state.df.empty:
    g_fotos = st.session_state.df[st.session_state.df['Foto'] != "Sin foto"]
    if not g_fotos.empty:
        st.divider()
        st.subheader("🔍 Consultar Comprobante")
        sel = st.selectbox("Seleccione el gasto:", g_fotos.apply(lambda x: f"{x['Fecha']} - {x['Descripción']}", axis=1))
        nom_f = g_fotos[g_fotos.apply(lambda x: f"{x['Fecha']} - {x['Descripción']}", axis=1) == sel]['Foto'].values[0]
        st.image(os.path.join(CARPETA_FOTOS, nom_f), width=500)

# Borrar (Solo Admin)
if es_admin and not st.session_state.df.empty:
    st.divider()
    if st.button("Eliminar Último Registro"):
        st.session_state.df = st.session_state.df.drop(st.session_state.df.index[-1])
        st.session_state.df.to_csv(ARCHIVO_DATOS, index=False)
        st.rerun()