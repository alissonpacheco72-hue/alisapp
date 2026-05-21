import time
import random
import os
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ------------------------------------------------------------------
# ⚠️ IMPORTANTE: Pon tu URL y Org de Grafana Cloud aquí
# ------------------------------------------------------------------
INFLUXDB_URL = "https://influx-prod-XX.grafana.net" # <-- CAMBIA ESTO
INFLUXDB_TOKEN = "TU_TOKEN_GRAFANA_AQUI"
INFLUXDB_ORG = "tu_org_aqui"                        # <-- CAMBIA ESTO
INFLUXDB_BUCKET = "sensor_data"                     # <-- Asegúrate que este bucket exista en Grafana Cloud

def run_simulation():
    print("🚀 Iniciando Simulador de Datos IoT para Grafana...")
    print(f"Conectando a {INFLUXDB_URL}...")
    
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        productos = ["PROD-001", "PROD-002", "PROD-003", "PROD-004", "PROD-005"]
        
        print("Generando 50 movimientos históricos simulados...")
        
        for i in range(50):
            prod = random.choice(productos)
            is_entry = random.choice([True, False])
            mov_type = "entrada" if is_entry else "salida"
            
            # Simulamos datos de las últimas 24 horas
            past_time = datetime.utcnow() - timedelta(minutes=random.randint(1, 1440))
            
            # Alarma: 30% de probabilidad si es salida
            is_alert = True if (not is_entry and random.random() < 0.3) else False

            point = Point("inventory_movement") \
                .tag("type", mov_type) \
                .tag("product_id", prod) \
                .field("quantity", 1) \
                .field("alert_triggered", is_alert) \
                .time(past_time, WritePrecision.NS)
                
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            
        print("✅ Simulación completada con éxito. Revisa Grafana Cloud.")
        
    except Exception as e:
        print(f"❌ Error al enviar datos: {e}")
        print("Asegúrate de haber puesto tu URL y ORG correctamente en este script.")

if __name__ == "__main__":
    run_simulation()
