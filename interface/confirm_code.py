import streamlit as st
import time
from controllers.sensor_controller import SensorController

def show():
    st.title("📷 Confirmar Lectura QR / Código de Barras")
    st.write("Esta sección simula la lectura física cuando el producto pasa por la puerta/sensor.")
    
    controller = SensorController()
    products_df = controller.get_all_products()
    
    if products_df.empty:
        st.warning("No hay productos en la base de datos para escanear.")
        return
        
    # Simulate a barcode scan
    product_options = products_df['id'] + " - " + products_df['name']
    selected = st.selectbox("Simulador de Código Detectado (Lector Wokwi):", product_options)
    
    product_id = selected.split(" - ")[0]
    product = controller.get_product(product_id)
    
    if product:
        st.markdown("### Detalles del Producto Detectado")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Nombre:** {product['name']}")
            st.write(f"**Categoría:** {product['category']}")
            
        with col2:
            status_color = "green" if product['status'] == "dentro" else "red"
            st.write(f"**Estado Actual:** :{status_color}[{product['status'].upper()}]")
            st.write(f"**Último Movimiento:** {product['last_movement']}")
            
        st.markdown("---")
        st.write("### Acción")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📥 Confirmar Entrada", use_container_width=True, type="primary"):
                success, msg = controller.process_entry(product_id)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)
        with c2:
            if st.button("📤 Confirmar Salida (Disparar Alarma)", use_container_width=True, type="primary"):
                success, msg = controller.process_exit(product_id, trigger_alert=True)
                if success:
                    st.error("🚨 SALIDA DETECTADA: " + msg)
                    st.toast('🚨 Activando LED y BUZZER...', icon='🚨')
                    # Visual trick for buzzer
                    with st.empty():
                        for i in range(3):
                            st.markdown(f"### 🔴 🔊 BEEP BEEP BEEP")
                            time.sleep(0.3)
                            st.markdown("")
                            time.sleep(0.3)
                else:
                    st.warning(msg)
