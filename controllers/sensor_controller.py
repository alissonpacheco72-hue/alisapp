from infrastructure.csv_repository import CSVRepository
from infrastructure.influxdb_repository import InfluxDBRepository
from use_cases.register_product import RegisterProductUseCase
from use_cases.confirm_entry import ConfirmEntryUseCase
from use_cases.confirm_exit import ConfirmExitUseCase
from use_cases.generate_alert import GenerateAlertUseCase

class SensorController:
    def __init__(self):
        self.csv_repo = CSVRepository()
        self.influx_repo = InfluxDBRepository()
        
        self.generate_alert_uc = GenerateAlertUseCase(self.csv_repo)
        self.register_product_uc = RegisterProductUseCase(self.csv_repo)
        self.confirm_entry_uc = ConfirmEntryUseCase(self.csv_repo, self.influx_repo)
        self.confirm_exit_uc = ConfirmExitUseCase(self.csv_repo, self.generate_alert_uc, self.influx_repo)

    def get_all_products(self):
        return self.csv_repo.get_all_products()
        
    def get_low_stock_products(self, threshold=5):
        df = self.get_all_products()
        if df.empty:
            return df
        return df[df['quantity'] < threshold]
        
    def get_product(self, product_id):
        return self.csv_repo.get_product(product_id)

    def get_all_movements(self):
        return self.csv_repo.get_all_movements()

    def get_all_alerts(self):
        return self.csv_repo.get_all_alerts()

    def register_product(self, product_id, name, category, quantity):
        return self.register_product_uc.execute(product_id, name, category, quantity)

    def process_entry(self, product_id):
        return self.confirm_entry_uc.execute(product_id)

    def process_exit(self, product_id, trigger_alert=True):
        return self.confirm_exit_uc.execute(product_id, requires_alert=trigger_alert)
        
    def mark_alert_reviewed(self, date_time, product_id):
        self.csv_repo.mark_alert_reviewed(date_time, product_id)
