import streamlit as st
import os

def show():
    st.title("🔌 Simulación IoT (Wokwi)")
    st.write("Según la rúbrica: *Simulación en Wokwi con un sensor conectado a un ESP32.*")
    
    st.markdown("""
    Esta vista representa la simulación IoT realizada en Wokwi. 
    ### Componentes del Circuito:
    - **ESP32**: Microcontrolador principal que procesa la lectura y envía los datos.
    - **PIR Motion Sensor (Lector QR simulado)**: Simula la detección física del producto pasando por la puerta.
    - **LED Rojo (Alarma Visual)**: Se enciende cuando hay una salida.
    - **Buzzer (Alarma Sonora)**: Suena al mismo tiempo que el LED.
    - **LCD 1602 (I2C)**: Muestra el estado actual ("ESCANEE QR").
    """)
    
    st.subheader("Representación Visual (Diagrama Wokwi)")
    
    image_path = "wokwi_circuit_diagram.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="Diagrama de conexiones Wokwi de los artefactos utilizados", use_column_width=True)
    else:
        st.warning("Imagen del diagrama no encontrada. Por favor asegúrate de que 'wokwi_circuit_diagram.png' esté en la raíz del proyecto.")
    
    st.markdown("---")
    st.subheader("Estado Interactivo Simulado")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="background-color:#2e2e2e; padding:20px; border-radius:10px; color:white; text-align:center;">
                <h3>ESP32</h3>
                <p>Status: ONLINE 🟢</p>
                <div style="border: 2px solid white; padding: 10px; margin: 10px;">
                    LCD 1602: "ESPERANDO LECTURA"
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col2:
        action = st.radio("Simular Detección del Sensor:", ("Reposo", "Entrada Detectada", "Salida Detectada"))
        
        if action == "Reposo":
            st.markdown("⬛ LED: APAGADO")
            st.markdown("🔈 Buzzer: SILENCIO")
        elif action == "Entrada Detectada":
            st.markdown("🟩 LED: APAGADO (Entrada normal)")
            st.markdown("🔈 Buzzer: BEEP CORTO (Confirmación)")
            st.success("✅ Datos enviados por HTTP (Simulado)")
        elif action == "Salida Detectada":
            st.markdown("🟥 LED: ENCENDIDO (Alarma)")
            st.markdown("🔊 Buzzer: SIRENA ACTIVADA")
            st.error("🚨 Datos de ALERTA enviados por HTTP")
