import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from app.config.settings import BOT_TOKEN
from app.config.logger import setup_logger
from app.bot.handlers import start_command, button_handler
from app.models.order import Order
from app.models.slot import Slot


logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error("Unhandled error: %s", context.error)


def main():
    setup_logger()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()