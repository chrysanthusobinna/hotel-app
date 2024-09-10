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

def view_all_guests():
    """
    Fetches and prints all guest entries from the spreadsheet.
    """
    rows = SHEET.worksheet(WORKSHEET).get_all_values()
    for row in rows:
        print(row)

def search_guest_by_email(email):
    """
    Search for a guest entry using their email address.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()  # Fetch all rows as dictionaries
    for record in records:
        if record["Email Address"] == email:
            return record
    return None


def update_guest(email, data_to_update):
    """
    Updates guest entry by searching for their email address.
    `data_to_update` should be a dictionary with updated fields.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    
    for idx, record in enumerate(records):
        if record["Email Address"] == email:
            row_number = idx + 2  # Row number in Google Sheets (1-based)
            for key, value in data_to_update.items():
                col_index = list(record.keys()).index(key) + 1  # Get the column index
                SHEET.worksheet(WORKSHEET).update_cell(row_number, col_index, value)
            print(f"Updated guest: {email}")
            return
    print(f"Guest with email {email} not found.")


data_to_update = {
    "Guest Name": "Chrys Obinna",
    "Phone Number": "08066554433",
    "Address": "London, UK",
    "Class of Room Booked": "Diamond",
    "Room Number": "9",
    "Amount Paid": "800"
}

update_guest("chrys@gmail.com", data_to_update)