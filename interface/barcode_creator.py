import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
from controllers.sensor_controller import SensorController

def show():
    st.title("🖨️ Crear Código QR para Producto Nuevo")
    
    controller = SensorController()
    
    with st.form("new_product_form"):
        st.subheader("Datos del Producto")
        product_id = st.text_input("Código (ID) del Producto", max_chars=20)
        name = st.text_input("Nombre del Producto")
        category = st.selectbox("Categoría", ["Electrónica", "Accesorios", "Mobiliario", "Suministros", "Otros"])
        quantity = st.number_input("Cantidad Inicial", min_value=1, value=1)
        
        submitted = st.form_submit_button("Registrar y Generar QR")
        
        if submitted:
            if not product_id or not name:
                st.error("Por favor completa el código y nombre del producto.")
            else:
                try:
                    # Register
                    controller.register_product(product_id, name, category, quantity)
                    st.success("Producto registrado exitosamente.")
                    
                    # Generate QR
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(product_id)
                    qr.make(fit=True)
                    
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    # Convert to bytes
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.markdown("### Código Generado")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(byte_im, caption=f"QR para {product_id}", width=200)
                    with col2:
                        st.download_button(
                            label="📥 Descargar Imagen QR",
                            data=byte_im,
                            file_name=f"{product_id}_qr.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"Error al registrar: {str(e)}")
