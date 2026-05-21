import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.sensor_controller import SensorController

def show():
    # Use HTML for a custom SaaS-like header with Online Status
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <h1 style="color: #1E293B; margin-bottom: 0;">Dashboard</h1>
                <p style="color: #64748B; font-size: 1.1rem; margin-top: 5px;">Monitor en tiempo real del inventario IoT.</p>
            </div>
            <div class="status-online">
                <span>ONLINE: SENSOR WOKWI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # IoT Visual Pipeline
    st.markdown("""
        <div class="pipeline-container">
            <div class="pipeline-step">
                <div class="pipeline-icon">📦</div>
                <div class="pipeline-text">1. Producto Pasa</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">📡</div>
                <div class="pipeline-text">2. Sensor Detecta</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">🚨</div>
                <div class="pipeline-text">3. Alarma / Acción</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">💻</div>
                <div class="pipeline-text">4. Streamlit Actualiza</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">☁️</div>
                <div class="pipeline-text">5. Grafana Recibe</div>
            </div>
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
    
    low_stock_df = controller.get_low_stock_products(threshold=5)
    low_stock_count = len(low_stock_df)
    
    # Toast Alert for recent activity
    if not alerts_df.empty:
        last_alert = alerts_df.iloc[-1]
        if last_alert['status'] == 'pendiente':
            st.toast(f"🚨 ALERTA ACTIVA: {last_alert['reason']} - Producto: {last_alert['product_id']}", icon="🚨")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
    with col5:
        delta_class = "delta-negative" if low_stock_count > 0 else "delta-positive"
        st.markdown(f"""
            <div class="custom-metric-card">
                <div class="custom-metric-title">Stock Bajo</div>
                <div class="custom-metric-value">{low_stock_count}</div>
                <div><span class="custom-metric-delta {delta_class}">Prod &lt; 5 unidades</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>📉 Tráfico en Tiempo Real</h3>", unsafe_allow_html=True)
        if not movements_df.empty:
            movements_df['date_time'] = pd.to_datetime(movements_df['date_time'])
            # Create a timeseries of events
            timeline = movements_df.groupby([movements_df['date_time'].dt.strftime('%m-%d %H:%M'), 'movement_type']).size().unstack(fill_value=0).reset_index()
            fig3 = px.line(timeline, x='date_time', y=timeline.columns[1:], markers=True, color_discrete_sequence=['#22C55E', '#F43F5E'])
            fig3.update_layout(margin=dict(t=20, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Tiempo", yaxis_title="Eventos")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No hay datos suficientes para el gráfico.")
            
    with col_chart2:
        st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>💻 Consola de Logs (En Vivo)</h3>", unsafe_allow_html=True)
        logs_html = "<div class='terminal-console'>"
        if not movements_df.empty:
            for _, row in movements_df.tail(15).iloc[::-1].iterrows():
                time_str = str(row['date_time']).split('.')[0][-8:]
                color_class = "log-error" if row['movement_type'] == 'salida' else "log-info"
                action = "SALIDA DETECTADA" if row['movement_type'] == 'salida' else "ENTRADA DETECTADA"
                logs_html += f"<div>[{time_str}] SENSOR: Producto {row['product_id']} -> <span class='{color_class}'>{action}</span> -> Enviando a Grafana...</div>"
        else:
            logs_html += "<div>Esperando conexión del sensor...</div>"
        logs_html += "</div>"
        st.markdown(logs_html, unsafe_allow_html=True)

    # Integrations Links
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>☁️ Integración IoT Externa</h3>", unsafe_allow_html=True)
    st.link_button("📊 Abrir Panel Analítico (Grafana Cloud)", "https://alissonpacheco72.grafana.net/goto/sbmfdh?orgId=stacks-1660538", type="primary", use_container_width=True)
