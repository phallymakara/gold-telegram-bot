from datetime import datetime
import requests

from app.services.google_client import orders_sheet
from app.models.order import Order


def create_order(order: Order):
    orders_sheet.append_row(
        [
            order.order_id,
            order.telegram_id,
            order.username,
            order.order_type,
            order.slot_date,
            order.premium,
            order.quantity_kg,
            order.status,
            datetime.now().isoformat(),
        ],
        value_input_option="USER_ENTERED",
        insert_data_option="INSERT_ROWS",
    )


def get_orders_by_telegram_id(telegram_id: str):
    try:
        rows = orders_sheet.get_all_records()

        return [
            row for row in rows
            if str(row["telegram_id"]) == str(telegram_id)
        ]

    except requests.exceptions.RequestException:
        return []