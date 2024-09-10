import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Load credentials
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPE)
client = gspread.authorize(creds)

# Open the spreadsheet by name
SHEET = client.open("Hotel Management")  # open spreadsheet 
WORKSHEET = SHEET.booking-record  # Access  booking-record sheet
