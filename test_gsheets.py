import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'my-jarvis-466409-f5089b992b67.json'

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Use your actual spreadsheet ID here
sheet = client.open_by_key("10dzawvYkrgooe57Pr0XHoWlxZXCVMsfepdHDSfSY3sY")
worksheet = sheet.worksheet("Habit")
worksheet.append_row(["Test", "Test", "Test"])
print("Success!")
