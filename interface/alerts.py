import streamlit as st
from controllers.sensor_controller import SensorController

def show():
    st.title("🚨 Gestión de Alertas")
    
    controller = SensorController()
    df = controller.get_all_alerts()
    
    if df.empty:
        st.info("No hay alertas registradas.")
        return
        
    st.subheader("Alertas Pendientes")
    pendientes = df[df['status'] == 'pendiente']
    
    if pendientes.empty:
        st.success("No hay alertas pendientes por revisar.")
    else:
        for index, row in pendientes.iterrows():
            with st.expander(f"🔴 Alerta {row['date_time']} - Producto: {row['product_id']}", expanded=True):
                st.write(f"**Motivo:** {row['reason']}")
                if st.button(f"Marcar como Revisada", key=f"btn_{index}"):
                    controller.mark_alert_reviewed(row['date_time'], row['product_id'])
                    st.rerun()

    st.markdown("---")
    st.subheader("Historial de Alertas Revisadas")
    revisadas = df[df['status'] == 'revisada']
    if not revisadas.empty:
        st.dataframe(revisadas, use_container_width=True, hide_index=True)
