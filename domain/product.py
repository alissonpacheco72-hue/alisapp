from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    category: str
    quantity: int
    status: str
    last_movement: str
