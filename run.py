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
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel-app')
WORKSHEET = "booking-record"




def add_guest(name, phone, address, email, room_class, room_number, amount_paid):
    """
    Adds a new guest entry to the spreadsheet.
    """
    guest_data = [name, phone, address, email, room_class, room_number, amount_paid]
    SHEET.worksheet(WORKSHEET).append_row(guest_data) 
    print(f"Added guest: {name}")


add_guest("chrys", "08026044909", "bolton, UK", "chrys@gmail.com", "Gold Room", "5", "500")
