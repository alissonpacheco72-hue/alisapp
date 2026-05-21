import pandas as pd
import os
from datetime import datetime

class CSVRepository:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.products_file = os.path.join(data_dir, "sample_data.csv")
        self.movements_file = os.path.join(data_dir, "movements.csv")
        self.alerts_file = os.path.join(data_dir, "alerts.csv")
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        if not os.path.exists(self.products_file):
            df = pd.DataFrame(columns=["id", "name", "category", "quantity", "status", "last_movement"])
            df.to_csv(self.products_file, index=False)
            
        if not os.path.exists(self.movements_file):
            df = pd.DataFrame(columns=["date_time", "product_id", "movement_type", "user"])
            df.to_csv(self.movements_file, index=False)
            
        if not os.path.exists(self.alerts_file):
            df = pd.DataFrame(columns=["date_time", "product_id", "reason", "status"])
            df.to_csv(self.alerts_file, index=False)

    def get_all_products(self):
        return pd.read_csv(self.products_file)

    def get_product(self, product_id):
        df = self.get_all_products()
        product = df[df["id"] == product_id]
        if not product.empty:
            return product.iloc[0].to_dict()
        return None

    def add_product(self, product_dict):
        df = self.get_all_products()
        # Convert dictionary to DataFrame line
        new_row = pd.DataFrame([product_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.products_file, index=False)

    def update_product_status(self, product_id, new_status, quantity_change=0):
        df = self.get_all_products()
        idx = df.index[df['id'] == product_id].tolist()
        if idx:
            df.at[idx[0], 'status'] = new_status
            df.at[idx[0], 'last_movement'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if quantity_change != 0:
                df.at[idx[0], 'quantity'] = int(df.at[idx[0], 'quantity']) + quantity_change
            df.to_csv(self.products_file, index=False)

    def add_movement(self, movement_dict):
        df = pd.read_csv(self.movements_file)
        new_row = pd.DataFrame([movement_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.movements_file, index=False)
        
    def get_all_movements(self):
        return pd.read_csv(self.movements_file)

    def add_alert(self, alert_dict):
        df = pd.read_csv(self.alerts_file)
        new_row = pd.DataFrame([alert_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.alerts_file, index=False)

    def get_all_alerts(self):
        return pd.read_csv(self.alerts_file)
        
    def mark_alert_reviewed(self, date_time, product_id):
        df = pd.read_csv(self.alerts_file)
        idx = df.index[(df['date_time'] == date_time) & (df['product_id'] == product_id)].tolist()
        if idx:
            df.at[idx[0], 'status'] = 'revisada'
            df.to_csv(self.alerts_file, index=False)
