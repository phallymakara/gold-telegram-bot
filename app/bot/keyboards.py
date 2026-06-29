from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants.callback import (
    BUY,
    SELL,
    MY_ORDERS,
    BACK_MAIN,
    BUY_SLOT_PREFIX,
    SELL_SLOT_PREFIX,
    QTY_PREFIX,
    CONFIRM_ORDER,
    CANCEL_ORDER,
)


MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🟢 BUY", callback_data=BUY),
        InlineKeyboardButton("🔴 SELL", callback_data=SELL),
    ],
    [
        InlineKeyboardButton("📋 My Orders", callback_data=MY_ORDERS),
    ],
])


def build_slot_keyboard(slots, order_type=BUY):
    keyboard = []

    prefix = BUY_SLOT_PREFIX if order_type == BUY else SELL_SLOT_PREFIX

    for slot in slots:
        keyboard.append([
            InlineKeyboardButton(
                f"📅 {slot['slot_date']} | +{slot['premium']} | {slot['stock_kg']}kg",
                callback_data=f"{prefix}{slot['slot_date']}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back to Main Menu", callback_data=BACK_MAIN)
    ])

    return InlineKeyboardMarkup(keyboard)


def build_quantity_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1 kg", callback_data=f"{QTY_PREFIX}1"),
            InlineKeyboardButton("2 kg", callback_data=f"{QTY_PREFIX}2"),
        ],
        [
            InlineKeyboardButton("3 kg", callback_data=f"{QTY_PREFIX}3"),
            InlineKeyboardButton("4 kg", callback_data=f"{QTY_PREFIX}4"),
        ],
        [
            InlineKeyboardButton("5 kg", callback_data=f"{QTY_PREFIX}5"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Slots", callback_data=BUY),
        ],
    ])


def build_confirmation_keyboard(selected_slot, order_type=BUY):
    prefix = BUY_SLOT_PREFIX if order_type == BUY else SELL_SLOT_PREFIX

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm", callback_data=CONFIRM_ORDER),
            InlineKeyboardButton("❌ Cancel", callback_data=CANCEL_ORDER),
        ],
        [
            InlineKeyboardButton(
                "⬅ Back to Quantity",
                callback_data=f"{prefix}{selected_slot}",
            ),
        ],
    ])


def build_back_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data=BACK_MAIN),
        ]
    ])