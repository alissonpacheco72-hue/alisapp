from datetime import datetime
from domain.product import Product
from infrastructure.csv_repository import CSVRepository

class RegisterProductUseCase:
    def __init__(self, repository: CSVRepository):
        self.repository = repository

    def execute(self, product_id, name, category, quantity):
        # Validate if exists
        existing = self.repository.get_product(product_id)
        if existing:
            raise ValueError(f"Product with ID {product_id} already exists.")
        
        new_product = Product(
            id=product_id,
            name=name,
            category=category,
            quantity=quantity,
            status="dentro",
            last_movement=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.repository.add_product(new_product.__dict__)
        return new_product
