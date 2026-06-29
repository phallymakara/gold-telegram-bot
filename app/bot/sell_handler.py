from app.bot.keyboards import build_slot_keyboard
from app.services.slot_service import get_active_slots


async def handle_sell(query):
    slots = get_active_slots()

    await query.edit_message_text(
        "Available SELL slots:\n\nPlease choose a slot:",
        reply_markup=build_slot_keyboard(slots, order_type="SELL"),
    )
