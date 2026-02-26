import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

# URL de respuesta de tu formulario de Google (Verificada)
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd92A98fvp-Eae8-wKGDoCwxRKjjkZyFOEVZzywBTb31mAQYQ/formResponse"

# ID de tu hoja de cálculo de Google (Verificado de tus capturas)
SHEET_ID = "1ORuU56oKeW7Y6pNgj--gX_-AYDxQAiZZFYnYEGBK-d8"

st.set_page_config(page_title="Mantenimiento Carlos Ortiz", layout="wide", page_icon="🛠️")

# Función para LEER los datos del Excel
def cargar_datos_nube():
    # Apuntamos a la pestaña de respuestas (gid=1791632682)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1791632682"
    try:
        df = pd.read_csv(url)
        # Limpiamos filas que no tengan descripción para evitar errores visuales
        if not df.empty and 'Descripción' in df.columns:
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
            
            # MAPEO DE CAMPOS (CUIDADO: No borrar ninguna comilla aquí)
            datos_enviar = {
                "entry.1593539825": id_u,
                "entry.1223947471": str(f),
                "entry.174092490": l,
                "entry.1802951965": d,
                "entry.1018596001": c,
                "entry.1989045768": str(m)
            }
            
            try:
                requests.post(URL_FORM, data=datos_enviar)
                st.success("¡Datos sincronizados con éxito!")
                # Recargar tabla inmediatamente
                st.session_state.df = cargar_datos_nube()
                st.rerun()
            except:
                st.error("Error al conectar con Google Sheets.")
else:
    st.sidebar.info("Introduzca la clave para habilitar el registro.")

# --- PANEL PRINCIPAL (Visualización) ---
st.write("---")

# Calcular total si hay datos
if not st.session_state.df.empty and "Monto" in st.session_state.df.columns:
    m_calc = pd.to_numeric(st.session_state.df["Monto"], errors='coerce').fillna(0)
    st.metric("Gasto Total Acumulado", f"S/ {m_calc.sum():,.2f}")

st.write("### 📋 Historial en Google Sheets")

if not st.session_state.df.empty:
    # Mostramos las columnas útiles
    columnas_vista = [col for col in ["Fecha", "Local", "Descripción", "Categoría", "Monto"] if col in st.session_state.df.columns]
    st.dataframe(st.session_state.df[columnas_vista], use_container_width=True)
else:
    st.info("No hay datos registrados todavía.")

# Botón para descargar respaldo
if not st.session_state.df.empty:
    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte CSV", csv, "reporte_mantenimiento.csv", "text/csv")


