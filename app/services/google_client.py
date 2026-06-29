import gspread
from google.oauth2.service_account import Credentials

from app.config.settings import (
    SPREADSHEET_ID,
    SERVICE_ACCOUNT_FILE,
    SCOPES,
)

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES,
)

client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SPREADSHEET_ID)

slots_sheet = spreadsheet.worksheet("Slots")
orders_sheet = spreadsheet.worksheet("Orders")