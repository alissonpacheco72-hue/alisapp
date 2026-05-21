from datetime import datetime
from domain.movement import Movement
from infrastructure.csv_repository import CSVRepository
# Optional InfluxDB integration could be called here via another repo

class ConfirmEntryUseCase:
    def __init__(self, repository: CSVRepository, influx_repo=None):
        self.repository = repository
        self.influx_repo = influx_repo

    def execute(self, product_id, user="System"):
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError("Product not found")
            
        if product["status"] == "dentro":
            return False, "El producto ya se encuentra dentro."

        # Update product status
        self.repository.update_product_status(product_id, "dentro")
        
        # Register movement
        mov = Movement(
            date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product_id=product_id,
            movement_type="entrada",
            user=user
        )
        self.repository.add_movement(mov.__dict__)
        
        # Log to InfluxDB if available
        if self.influx_repo:
            self.influx_repo.log_movement("entrada", product_id)
            
        return True, "Entrada registrada correctamente."
