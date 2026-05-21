import streamlit as st
from interface import dashboard, confirm_code, inventory, movements, alerts, diagram, barcode_creator

st.set_page_config(
    page_title="Sensor de Stock - IoT",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.sidebar.title("📦 Sensor de Stock")
st.sidebar.markdown("Sistema de Control IoT")

menu = st.sidebar.radio(
    "Navegación",
    [
        "Dashboard Principal",
        "Confirmar Lector",
        "Inventario",
        "Movimientos",
        "Alertas",
        "Simulador Wokwi",
        "Crear QR / Código"
    ]
)

if menu == "Dashboard Principal":
    dashboard.show()
elif menu == "Confirmar Lector":
    confirm_code.show()
elif menu == "Inventario":
    inventory.show()
elif menu == "Movimientos":
    movements.show()
elif menu == "Alertas":
    alerts.show()
elif menu == "Simulador Wokwi":
    diagram.show()
elif menu == "Crear QR / Código":
    barcode_creator.show()

st.sidebar.markdown("---")
st.sidebar.info("Proyecto de IoT Integrado al Análisis de Datos.")
