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

# Append a row to the worksheet with explicit column positioning
def append_row(row_values, worksheet=0):
    ws = open_sheet(worksheet)
    # Convert row_values to a list if it's not already
    if not isinstance(row_values, list):
        row_values = [row_values]
    
    # Get all values to find the next empty row
    all_values = ws.get_all_values()
    next_row = len(all_values) + 1
    
    # Write each value to the correct column (A, C, E, G)
    column_mapping = ['A', 'C', 'E', 'G']
    for i, value in enumerate(row_values):
        if i < len(column_mapping):
            cell_address = f"{column_mapping[i]}{next_row}"
            # Use the correct format for ws.update()
            ws.update(cell_address, [[value]])

# Read all rows from the worksheet
def get_all_rows(worksheet=0):
    ws = open_sheet(worksheet)
    return ws.get_all_values() 