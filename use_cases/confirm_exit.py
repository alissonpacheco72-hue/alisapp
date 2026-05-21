from datetime import datetime
from domain.movement import Movement
from use_cases.generate_alert import GenerateAlertUseCase
from infrastructure.csv_repository import CSVRepository

class ConfirmExitUseCase:
    def __init__(self, repository: CSVRepository, alert_use_case: GenerateAlertUseCase, influx_repo=None):
        self.repository = repository
        self.alert_use_case = alert_use_case
        self.influx_repo = influx_repo

    def execute(self, product_id, user="System", requires_alert=False):
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError("Product not found")
            
        if product["status"] == "fuera":
            return False, "El producto ya se encuentra fuera."

        # Update product status
        self.repository.update_product_status(product_id, "fuera")
        
        # Register movement
        mov = Movement(
            date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product_id=product_id,
            movement_type="salida",
            user=user
        )
        self.repository.add_movement(mov.__dict__)
        
        # Log to InfluxDB if available
        if self.influx_repo:
            self.influx_repo.log_movement("salida", product_id)
            
        # Generate Alert if needed (e.g. unauthorized exit or just any exit)
        if requires_alert:
            self.alert_use_case.execute(product_id, "Salida detectada por sensor")
            
        return True, "Salida registrada correctamente."
