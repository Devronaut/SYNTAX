import gspread
from google.oauth2.service_account import Credentials

# If your service account file is named differently, update the filename below
SERVICE_ACCOUNT_FILE = 'my-jarvis-466409-f5089b992b67.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SPREADSHEET_ID = '10dzawvYkrgooe57Pr0XHoWlxZXCVMsfepdHDSfSY3sY'

# Authenticate and return a gspread client
def get_gspread_client():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return gspread.authorize(creds)

# Open a Google Sheet by name and return the worksheet (tab) by name or index
def open_sheet(worksheet=0):
    client = get_gspread_client()
    sheet = client.open_by_key(SPREADSHEET_ID)
    if isinstance(worksheet, int):
        return sheet.get_worksheet(worksheet)
    else:
        return sheet.worksheet(worksheet)

# Append a row to the worksheet
def append_row(row_values, worksheet=0):
    ws = open_sheet(worksheet)
    ws.append_row(row_values)

# Read all rows from the worksheet
def get_all_rows(worksheet=0):
    ws = open_sheet(worksheet)
    return ws.get_all_values() 