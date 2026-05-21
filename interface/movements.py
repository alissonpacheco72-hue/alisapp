import streamlit as st
from controllers.sensor_controller import SensorController

def show():
    st.title("🔄 Registro de Movimientos")
    
    controller = SensorController()
    df = controller.get_all_movements()
    
    if df.empty:
        st.info("No hay movimientos registrados.")
        return
        
    st.dataframe(
        df,
        column_config={
            "date_time": "Fecha y Hora",
            "product_id": "Código Producto",
            "movement_type": "Tipo Movimiento",
            "user": "Usuario Responsable",
        },
        hide_index=True,
        use_container_width=True
    )
