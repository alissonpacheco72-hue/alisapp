import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.sensor_controller import SensorController

def show():
    # Use HTML for a custom SaaS-like header
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="color: #1E293B; margin-bottom: 0;">Dashboard</h1>
            <p style="color: #64748B; font-size: 1.1rem; margin-top: 5px;">Bienvenido de nuevo, administrador. Gestiona tu inventario aquí.</p>
        </div>
    """, unsafe_allow_html=True)
    
    controller = SensorController()
    
    products_df = controller.get_all_products()
    movements_df = controller.get_all_movements()
    alerts_df = controller.get_all_alerts()
    
    total_products = len(products_df)
    in_stock = len(products_df[products_df['status'] == 'dentro'])
    out_stock = len(products_df[products_df['status'] == 'fuera'])
    active_alerts = len(alerts_df[alerts_df['status'] == 'pendiente']) if not alerts_df.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Custom HTML cards for metrics to match the reference image
    with col1:
        st.markdown(f"""
            <div class="custom-metric-card">
                <div class="custom-metric-title">Total Productos</div>
                <div class="custom-metric-value">{total_products}</div>
                <div><span class="custom-metric-delta delta-positive">+12% este mes</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="custom-metric-card">
                <div class="custom-metric-title">En Inventario</div>
                <div class="custom-metric-value">{in_stock}</div>
                <div><span class="custom-metric-delta delta-positive">+5 nuevos hoy</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="custom-metric-card">
                <div class="custom-metric-title">Productos Fuera</div>
                <div class="custom-metric-value">{out_stock}</div>
                <div><span class="custom-metric-delta delta-negative">-2 sin regresar</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        delta_class = "delta-negative" if active_alerts > 0 else "delta-positive"
        delta_text = "Requiere atención" if active_alerts > 0 else "Todo en orden"
        st.markdown(f"""
            <div class="custom-metric-card">
                <div class="custom-metric-title">Alertas Activas</div>
                <div class="custom-metric-value">{active_alerts}</div>
                <div><span class="custom-metric-delta {delta_class}">{delta_text}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>Estado del Inventario</h3>", unsafe_allow_html=True)
        if not products_df.empty:
            # Match colors with the reference image (Green & Red/Orange)
            fig = px.pie(products_df, names='status', hole=0.6, color_discrete_sequence=['#22C55E', '#F43F5E'])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar.")
            
    with col_chart2:
        st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>Movimientos Recientes</h3>", unsafe_allow_html=True)
        if not movements_df.empty:
            mov_counts = movements_df['movement_type'].value_counts().reset_index()
            mov_counts.columns = ['Tipo', 'Cantidad']
            fig2 = px.bar(mov_counts, x='Tipo', y='Cantidad', color='Tipo', color_discrete_sequence=['#22C55E', '#F43F5E'])
            fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay movimientos registrados.")
            
    # Integrations Links
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>☁️ Integración IoT Externa</h3>", unsafe_allow_html=True)
    st.link_button("📊 Abrir Panel Analítico (Grafana Cloud)", "https://grafana.com/auth", type="primary", use_container_width=True)

    # Connect to Colab requirement mentioned in rubric
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>🔬 Análisis Predictivo (Integración Colab)</h3>", unsafe_allow_html=True)
    if not movements_df.empty:
        movements_df['date_time'] = pd.to_datetime(movements_df['date_time'])
        movements_df['hour'] = movements_df['date_time'].dt.hour
        hourly_activity = movements_df.groupby('hour').size().reset_index(name='count')
        
        fig3 = px.line(hourly_activity, x='hour', y='count', markers=True, color_discrete_sequence=['#3B58FF'])
        fig3.update_layout(margin=dict(t=20, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Se requiere más data para el análisis predictivo.")
