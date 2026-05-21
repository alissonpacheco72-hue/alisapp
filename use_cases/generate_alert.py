from datetime import datetime
from domain.alert import Alert
from infrastructure.csv_repository import CSVRepository

class GenerateAlertUseCase:
    def __init__(self, repository: CSVRepository):
        self.repository = repository

    def execute(self, product_id, reason):
        alert = Alert(
            date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product_id=product_id,
            reason=reason,
            status="pendiente"
        )
        self.repository.add_alert(alert.__dict__)
        return alert
