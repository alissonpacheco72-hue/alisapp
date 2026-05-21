from dataclasses import dataclass

@dataclass
class Alert:
    date_time: str
    product_id: str
    reason: str
    status: str
