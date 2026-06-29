from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

# buy handler
from app.bot.buy_handler import (
    handle_buy,
)

# order flow
from app.bot.order_flow import (
    handle_slot_selection,
    handle_quantity_selection,
    handle_confirm_order,
)

# sale handler
from app.bot.sell_handler import (
    handle_sell,
)

# order handler
from app.bot.order_handler import (
    handle_my_orders
)

from app.bot.keyboards import (
    LANG_MENU,
    build_main_menu,
    build_slot_keyboard,
    build_quantity_keyboard,
    build_confirmation_keyboard,
    build_back_main_keyboard,
)
from app.utils.translation import t
from app.services.order_service import place_buy_order, place_sell_order
from app.services.whitelist_service import restricted

from app.constants.callback import (
    BUY,
    SELL,
    MY_ORDERS,
    BACK_MAIN,
    CONFIRM_ORDER,
    CANCEL_ORDER,
    BUY_SLOT_PREFIX,
    SELL_SLOT_PREFIX,
    QTY_PREFIX,
)


@restricted
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        t("choose_lang", "EN"),
        reply_markup=LANG_MENU,
    )


@restricted
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        await query.answer()
    except BadRequest:
        pass

    if query.data.startswith("LANG_"):
        lang = query.data.replace("LANG_", "")
        context.user_data["lang"] = lang
        await query.message.reply_text(
            t("welcome", lang),
            reply_markup=build_main_menu(lang),
        )

    elif query.data == "SWITCH_LANG":
        await query.message.reply_text(
            t("choose_lang", "EN"),
            reply_markup=LANG_MENU,
        )

    elif query.data == BUY:   
        await handle_buy(query, context)

    elif query.data.startswith(BUY_SLOT_PREFIX) or query.data.startswith(SELL_SLOT_PREFIX):
        await handle_slot_selection(query, context)

    elif query.data.startswith(QTY_PREFIX):
        await handle_quantity_selection(query, context)

    elif query.data == CONFIRM_ORDER:
        await handle_confirm_order(update, query, context)

    elif query.data == CANCEL_ORDER:
        await handle_cancel_order(query, context)

    elif query.data == BACK_MAIN:
        await handle_back_main(query, context)

    elif query.data == SELL:
        await handle_sell(query, context)

    elif query.data == MY_ORDERS:
        await handle_my_orders(update, query, context)


async def handle_cancel_order(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "EN")
    context.user_data.clear()
    context.user_data["lang"] = lang
    await query.message.reply_text(t("order_cancelled", lang))


async def handle_back_main(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "EN")
    context.user_data.clear()
    context.user_data["lang"] = lang
    await query.message.reply_text(
        t("welcome", lang),
        reply_markup=build_main_menu(lang),
    )
