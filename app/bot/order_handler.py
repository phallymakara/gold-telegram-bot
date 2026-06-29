from telegram import Update

from app.bot.keyboards import build_back_main_keyboard
from app.services.order_sheet_service import get_orders_by_telegram_id


async def handle_my_orders(update: Update, query):
    user = update.effective_user

    orders = get_orders_by_telegram_id(str(user.id))

    if not orders:
        await query.edit_message_text(
            "📋 My Orders\n\n"
            "You do not have any orders yet.",
            reply_markup=build_back_main_keyboard(),
        )
        return

    message = "📋 My Orders\n\n"

    for order in orders[-5:]:
        message += (
            f"Order ID: {order['order_id']}\n"
            f"Type: {order['order_type']}\n"
            f"Slot: {order['slot_date']}\n"
            f"Premium: +{order['premium']}\n"
            f"Quantity: {order['quantity_kg']} kg\n"
            f"Status: {order['status']}\n"
            "──────────────\n"
        )

    await query.edit_message_text(
        message,
        reply_markup=build_back_main_keyboard(),
    )

    