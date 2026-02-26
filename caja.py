import streamlit as st
import pandas as pd
from datetime import date

# --- CONFIGURACIÓN ---
CLAVE_ADMIN = "jess7386"

st.set_page_config(page_title="Ortiz Mantenimiento", layout="wide", page_icon="🛠️")

# --- ESTILO DE ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    h1, h2, h3, p, span {
        color: #FFFFFF !important;
    }
    div[data-testid="stMetric"] {
        background-color: #1E2130;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3E44FE;
        box-shadow:




