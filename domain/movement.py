from dataclasses import dataclass

@dataclass
class Movement:
    date_time: str
    product_id: str
    movement_type: str
    user: str
