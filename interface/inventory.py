import streamlit as st
import pandas as pd
import time
from controllers.sensor_controller import SensorController

def show():
    st.title("📦 Inventario de Productos (Modo Excel / Sheets)")
    st.write("Modifica los datos directamente en la tabla y guárdalos. También puedes exportar o importar el archivo CSV completo.")
    
    controller = SensorController()
    
    # Export and Import section
    st.markdown("### 📤 Importar / 📥 Exportar / 🗄️ Base de Datos")
    col_up, col_down, col_db = st.columns(3)
    
    df_current = controller.get_all_products()
    csv_data = df_current.to_csv(index=False).encode('utf-8')
    
    with col_down:
        st.download_button(
            label="Descargar CSV",
            data=csv_data,
            file_name="productos_inventario.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with col_up:
        uploaded_file = st.file_uploader("Subir CSV para actualizar la base de datos", type=["csv"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Actualizar BD", use_container_width=True, type="primary"):
                try:
                    new_df = pd.read_csv(uploaded_file)
                    new_df.to_csv(controller.csv_repo.products_file, index=False)
                    st.success("¡BD actualizada!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    with col_db:
        st.link_button("🗄️ Administrar InfluxDB", "https://grafana.com/auth", use_container_width=True)
                    
    st.markdown("---")
    st.subheader("📝 Edición Rápida (Modo Excel)")
    
    # We must reload data in case it was just updated
    df = controller.get_all_products()
    
    if df.empty:
        st.info("No hay productos registrados en el inventario.")
        return
        
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Buscar por Nombre o Código", "")
    with col2:
        status_filter = st.selectbox("Filtrar por Estado", ["Todos", "dentro", "fuera"])
        
    # Apply filters visually (we only allow editing the full dataframe to avoid index mismatches on save)
    # But for a simple prototype, we'll edit the full dataframe and just use filters for viewing if they want, 
    # but st.data_editor handles sorting/filtering natively if configured.
    
    st.markdown(f"**Total de registros:** {len(df)}")
    
    # Create the data editor
    edited_df = st.data_editor(
        df,
        column_config={
            "id": st.column_config.TextColumn("Código QR", disabled=True), # usually IDs shouldn't change
            "name": "Nombre",
            "category": st.column_config.SelectboxColumn("Categoría", options=["Electrónica", "Accesorios", "Mobiliario", "Suministros", "Otros"]),
            "quantity": st.column_config.NumberColumn("Cantidad", format="%d", min_value=0),
            "status": st.column_config.SelectboxColumn("Estado", options=["dentro", "fuera"]),
            "last_movement": st.column_config.TextColumn("Último Movimiento", disabled=True),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    if st.button("💾 Guardar Cambios Realizados", type="primary"):
        # Save the edited dataframe back to the CSV
        edited_df.to_csv(controller.csv_repo.products_file, index=False)
        st.success("¡Cambios guardados correctamente!")
        time.sleep(1)
        st.rerun()
