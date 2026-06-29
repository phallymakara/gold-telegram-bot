from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    telegram_id: str
    username: str
    order_type: str
    slot_date: str
    premium: float
    quantity_kg: float
    status: str

    def to_row(self):
        return [
            self.order_id,
            self.telegram_id,
            self.username,
            self.order_type,
            self.slot_date,
            self.premium,
            self.quantity_kg,
            self.status,
        ]