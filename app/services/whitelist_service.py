import time
import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
import gspread

from app.services.google_client import spreadsheet
from app.utils.translation import t

logger = logging.getLogger(__name__)

# Cache configuration
_cached_users = set()
_last_fetch_time = 0
CACHE_TTL = 300  # 5 minutes in seconds
MAX_USERS = 2000  # Cap whitelist size to limit memory consumption

def get_whitelist_sheet():
    try:
        return spreadsheet.worksheet("Whitelist")
    except gspread.exceptions.WorksheetNotFound:
        # Auto-create the Whitelist worksheet if it doesn't exist
        sheet = spreadsheet.add_worksheet(title="Whitelist", rows="100", cols="2")
        sheet.append_row(["username", "telegram_id"])
        return sheet

def load_whitelist(force_refresh=False) -> set:
    global _cached_users, _last_fetch_time
    current_time = time.time()
    
    if not force_refresh and (current_time - _last_fetch_time < CACHE_TTL):
        return _cached_users
        
    try:
        sheet = get_whitelist_sheet()
        records = sheet.get_all_records()
        
        allowed = set()
        # Cap to MAX_USERS to guarantee memory stays low
        for row in records[:MAX_USERS]:
            username = str(row.get("username", "")).strip().lower().lstrip("@")
            if username:
                allowed.add(username)
                
            telegram_id = str(row.get("telegram_id", "")).strip()
            if telegram_id:
                allowed.add(telegram_id)
                
        _cached_users = allowed
        _last_fetch_time = current_time
        logger.info("Whitelist loaded/refreshed: %d allowed targets", len(_cached_users))
    except Exception as e:
        logger.error("Failed to load whitelist from Google Sheets: %s", e)
        # Keep old cache on error to keep the bot functioning
        
    return _cached_users

def is_user_allowed(username: str, telegram_id: str) -> bool:
    allowed_list = load_whitelist()
    
    clean_username = username.strip().lower().lstrip("@") if username else ""
    str_tg_id = str(telegram_id).strip()
    
    return (clean_username in allowed_list) or (str_tg_id in allowed_list)

def restricted(func):
    """
    Decorator for handlers to restrict access to whitelisted users.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user:
            return
            
        username = user.username
        telegram_id = str(user.id)
        
        if not is_user_allowed(username, telegram_id):
            logger.warning(
                "Unauthorized access attempt blocked | user_id=%s | username=%s",
                telegram_id,
                username,
            )
            
            lang = context.user_data.get("lang", "EN")
            unauth_msg = t("unauthorized", lang)
            
            # Respond appropriately depending on update type
            if update.callback_query:
                # For buttons, show alert popup
                await update.callback_query.answer(unauth_msg, show_alert=True)
            elif update.message:
                # For text/commands, reply to the message
                await update.message.reply_text(unauth_msg)
            return
            
        return await func(update, context, *args, **kwargs)
    return wrapper
