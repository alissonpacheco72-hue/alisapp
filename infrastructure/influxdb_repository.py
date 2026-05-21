from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

class InfluxDBRepository:
    def __init__(self):
        # Parametros para conectarse a Grafana Cloud (InfluxDB endpoint)
        self.url = os.getenv("INFLUXDB_URL", "https://influx-prod-XX.grafana.net") # NOTA: Cambia esto por tu URL de InfluxDB en Grafana Cloud
        self.token = os.getenv("INFLUXDB_TOKEN", "TU_TOKEN_GRAFANA_AQUI")
        self.org = os.getenv("INFLUXDB_ORG", "grafana_cloud_user_id") # Reemplaza con tu ID de usuario de Grafana Cloud
        self.bucket = os.getenv("INFLUXDB_BUCKET", "sensor_data")
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.is_connected = True
        except Exception as e:
            print(f"Error connecting to InfluxDB: {e}")
            self.is_connected = False

    def log_movement(self, movement_type, product_id):
        if not self.is_connected:
            return False
            
        try:
            point = Point("inventory_movement") \
                .tag("product_id", product_id) \
                .tag("movement_type", movement_type) \
                .field("value", 1 if movement_type == "entrada" else -1)
                
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            return True
        except Exception as e:
            print(f"Failed to write to InfluxDB: {e}")
            return False
