import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

# URL de respuesta de tu formulario
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd92A98fvp-Eae8-wKGDoCwxRKjjkZyFOEVZzywBTb31mAQYQ/formResponse"

# ID de tu Excel (Extraído de tu link)
SHEET_ID = "1ORuU56oKeW7Y6pNgj--gX_-AYDxQAiZZFYnYEGBK-d8"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para LEER los datos del Excel
def cargar_datos_nube():
    # Usamos la hoja específica de respuestas (gid=1791632682)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1791632682"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["Marca temporal", "ID", "Fecha", "Local", "Descripción", "Categoría", "Monto"])

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos_nube()

st.title("🛠️ Caja Chica Carlos Ortiz Mantenimiento")

# --- REGISTRO (Solo con clave) ---
st.sidebar.title("🔐 Acceso")
pass_input = st.sidebar.text_input("Clave:", type="password")

if pass_input == CLAVE_ADMIN:
    st.sidebar.success("✅ Modo Edición Activo")
    with st.sidebar.form("registro", clear_on_submit=True):
        st.header("📝 Nuevo Registro")
        f = st.date_input("Fecha", date.today())
        l = st.text_input("N° de Local")
        d = st.text_input("Descripción del gasto")
        c = st.selectbox("Categoría", ["Movilidad", "Alimentación", "Gasto de local", "Otros"])
        m = st.number_input("Monto (S/)", min_value=0.0, step=0.10)
        
        # Botón de guardar
        if st.form_submit_button("💾 Guardar en Google Sheets"):
            id_u = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
            
            # Mapeo exacto de los campos de tu formulario
            datos_enviar = {
                "entry.1593539825": id_u,        # Pregunta: ID
                "entry.1223947471": str(f),     # Pregunta: Fecha
                "entry.174092490": l,           # Pregunta: Local
                "entry.1802951965": d,          # Pregunta: Descripción
                "entry.1018596001": c,          # Pregunta: Categoría
                "entry.1989045768": str(m)      # Pregunta: Monto
            }
            
            try:
                # Envío invisible al formulario
                requests.post(URL_FORM, data=datos_enviar)
                st.success("¡Datos sincronizados correctamente!")
                # Recargar datos y refrescar la app
                st.session_state.df = cargar_datos_nube()
                st.rerun()
            except:
                st.error("Error al conectar con Google. Verifica tu internet.")

# --- VISUALIZACIÓN ---
st.write("---")
if not st.session_state.df.empty:
    # Limpiar columna de Monto para el cálculo
    if "Monto" in st.session_state.df.columns:
        monto_calc = pd.to_numeric(st.session_state.df["Monto"], errors='coerce').fillna(0)
        total = monto_calc.sum()
        
        c1, c2 = st.columns(2)
        c1.metric("Gasto Total Acumulado", f"S/ {total:,.2f}")
        c2.metric("Registros en Nube", len(st.session_state.df))

st.write("### 📋 Historial en Google Sheets")
# Mostrar la tabla (quitamos columnas innecesarias para la vista)
cols_a_mostrar = [c for c in st.session_state.df.columns if c not in ["Marca temporal", "ID"]]
st.dataframe(st.session_state.df[cols_a_mostrar] if not st.session_state.df.empty else st.session_state.df, use_container_width=True)

# Botón de descarga manual (Backup)
if not st.session_state.df.empty:
    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte CSV", csv, "reporte_mantenimiento.csv", "text/csv")

