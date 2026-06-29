from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards import (
    build_slot_keyboard,
    build_quantity_keyboard,
    build_confirmation_keyboard,
)

from app.bot.messages import (
    BUY_SLOT_MESSAGE,
    SESSION_EXPIRED_MESSAGE,
    SLOT_NOT_FOUND_MESSAGE,
)

from app.services.slot_service import (
    get_active_slots,
    get_slot_by_date,
)

from app.services.order_service import place_buy_order, place_sell_order


async def handle_buy(query):
    slots = get_active_slots()

    await query.edit_message_text(
        BUY_SLOT_MESSAGE,
        reply_markup=build_slot_keyboard(slots, order_type="BUY"),
    )


async def handle_slot_selection(query, context: ContextTypes.DEFAULT_TYPE):
    if query.data.startswith("BUY_SLOT_"):
        order_type = "BUY"
        slot_date = query.data.replace("BUY_SLOT_", "")
    else:
        order_type = "SELL"
        slot_date = query.data.replace("SELL_SLOT_", "")

    context.user_data["selected_slot"] = slot_date
    context.user_data["order_type"] = order_type

    await query.edit_message_text(
        f"You selected {order_type} slot: {slot_date}\n\n"
        "Please choose quantity:",
        reply_markup=build_quantity_keyboard(),
    )


async def handle_quantity_selection(query, context: ContextTypes.DEFAULT_TYPE):
    quantity = float(query.data.replace("QTY_", ""))

    selected_slot = context.user_data.get("selected_slot")
    order_type = context.user_data.get("order_type", "BUY")

    if not selected_slot:
        await query.edit_message_text(SESSION_EXPIRED_MESSAGE)
        return

    slot = get_slot_by_date(selected_slot)

    if not slot:
        await query.edit_message_text(SLOT_NOT_FOUND_MESSAGE)
        return

    context.user_data["quantity"] = quantity

    await query.edit_message_text(
        "📋 Order Summary\n\n"
        f"Type: {order_type}\n"
        f"Slot: {selected_slot}\n"
        f"Premium: +{slot['premium']}\n"
        f"Quantity: {quantity} kg\n\n"
        "Please confirm your order.",
        reply_markup=build_confirmation_keyboard(selected_slot),
    )


async def handle_confirm_order(
    update: Update,
    query,
    context: ContextTypes.DEFAULT_TYPE,
):
    selected_slot = context.user_data.get("selected_slot")
    quantity = context.user_data.get("quantity")
    order_type = context.user_data.get("order_type", "BUY")

    if not selected_slot or not quantity:
        await query.edit_message_text(SESSION_EXPIRED_MESSAGE)
        return

    user = update.effective_user

    try:
        if order_type == "BUY":
            order = place_buy_order(
                telegram_id=str(user.id),
                username=user.username or user.first_name or "unknown",
                slot_date=selected_slot,
                quantity=quantity,
            )
        else:
            order = place_sell_order(
                telegram_id=str(user.id),
                username=user.username or user.first_name or "unknown",
                slot_date=selected_slot,
                quantity=quantity,
            )

        context.user_data.clear()

        await query.edit_message_text(
            "✅ Order confirmed successfully!\n\n"
            f"Order ID: {order['order_id']}\n"
            f"Type: {order['order_type']}\n"
            f"Slot: {order['slot_date']}\n"
            f"Premium: +{order['premium']}\n"
            f"Quantity: {order['quantity_kg']} kg"
        )

    except ValueError as error:
        await query.edit_message_text(f"❌ {error}")