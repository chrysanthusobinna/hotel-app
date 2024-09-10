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


def delete_guest(email):
    """
    Deletes guest entry by searching for their email address.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    
    for idx, record in enumerate(records):
        if record["Email Address"] == email:
            row_number = idx + 2  # Row number in Google Sheets (1-based)
            SHEET.worksheet(WORKSHEET).delete_rows(row_number)
            print(f"Deleted guest with email: {email}")
            return
    print(f"Guest with email {email} not found.")


def main():
    """
    Displays a menu and handles user input.
    """
    while True:
        print("\nHotel Management System")
        print("1. Add Guest")
        print("2. View All Guests")
        print("3. Search Guest by Email")
        print("4. Update Guest")
        print("5. Delete Guest")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter guest name: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")
            email = input("Enter email: ")
            room_class = input("Enter room class: ")
            room_number = input("Enter room number: ")
            amount_paid = input("Enter amount paid: ")
            add_guest(name, phone, address, email, room_class, room_number, amount_paid)
        
        elif choice == "2":
            view_all_guests()
        
        elif choice == "3":
            email = input("Enter guest email to search: ")
            guest = search_guest_by_email(email)
            if guest:
                print(guest)
            else:
                print("Guest not found.")
        
        elif choice == "4":
            email = input("Enter guest email to update: ")
            updated_data = {}
            if input("Update name? (y/n): ") == "y":
                updated_data["Guest Name"] = input("Enter new name: ")
            if input("Update phone? (y/n): ") == "y":
                updated_data["Phone Number"] = input("Enter new phone: ")
            if input("Update address? (y/n): ") == "y":
                updated_data["Address"] = input("Enter new address: ")
            if input("Update room class? (y/n): ") == "y":
                updated_data["Class of Room Booked"] = input("Enter new room class: ")
            if input("Update room number? (y/n): ") == "y":
                updated_data["Room Number"] = input("Enter new room number: ")
            if input("Update amount paid? (y/n): ") == "y":
                updated_data["Amount Paid"] = input("Enter new amount: ")
            update_guest(email, updated_data)
        
        elif choice == "5":
            email = input("Enter guest email to delete: ")
            delete_guest(email)
        
        elif choice == "6":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, try again.")

# Start the program
main()