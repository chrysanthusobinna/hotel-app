import os
import re
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

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


def clear():
    """
    Clear function to clean-up the terminal so things don't get messy.
    """
    os.system("cls" if os.name == "nt" else "clear")


def is_valid_name(name):
    trimmed_name = name.strip()
    if not trimmed_name:
        return False
    for part in trimmed_name.split():
        if not all(char.isalpha() or char == '-' for char in part):
            return False
    return True


def is_valid_phone(phone):
    # A simple regex for validating phone numbers (adjust as needed)
    phone_str = str(phone)  # Ensure the phone number is a string
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone_str))


def is_valid_address(address):
    return bool(address.strip())  # Basic check: not empty


def is_valid_email(email):
    # Simple regex for validating email format
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))  # noqa


def email_exists(email):
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    # Iterate through each record to check for the email
    for record in records:
        if record.get('Email Address') == email:
            return True
    return False


def is_valid_room_class(room_class):
    accepted_classes = {'single', 'double', 'suite'}
    return room_class.lower() in accepted_classes


def is_valid_room_number(room_number):
    room_number_str = str(room_number)
    return room_number_str.isdigit() and int(room_number_str) > 0


def is_valid_amount_paid(amount_paid):
    try:
        float_amount = float(amount_paid)
        return float_amount >= 0
    except ValueError:
        return False


def add_guest(
        name, phone, address, email, room_class, room_number, amount_paid):
    """
    Adds a new guest entry to the spreadsheet.
    """
    guest_data = [
            name, phone, address, email, room_class, room_number, amount_paid]
    SHEET.worksheet(WORKSHEET).append_row(guest_data)
    clear()
    print(f"Added guest: {name}\n")
    input("Press Enter to Continue\n")


def view_all_guests():
    """
    Fetches and prints all guest entries
    from the spreadsheet using PrettyTable.
    """
    rows = SHEET.worksheet(WORKSHEET).get_all_values()
    if not rows:
        print("No data available.")
        return
    table = PrettyTable()
    table.field_names = rows[0]
    for row in rows[1:]:
        table.add_row(row)
    print(table)
    input("Press Enter to Continue\n")


def search_guest_by_email(email):
    """
    Search for a guest entry using their email address and display the result.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    for record in records:
        if record["Email Address"] == email:
            table = PrettyTable()
            table.field_names = record.keys()
            table.add_row(record.values())
            print(table)
            return record
    print("Guest not found.")
    return None


def get_guest_record_by_email(email):
    """
    Search for a guest record using their email address
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    for record in records:
        if record["Email Address"] == email:
            return record
    print("Guest not found.")
    return None


def update_guest(email, data_to_update):
    """
    Updates guest entry by searching for their email address.
    `data_to_update` should be a dictionary with updated fields.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    for idx, record in enumerate(records):
        if record["Email Address"] == email:
            row_number = idx + 2
            for key, value in data_to_update.items():
                col_index = list(record.keys()).index(key) + 1
                SHEET.worksheet(WORKSHEET).update_cell(row_number, col_index, value)  # noqa
            print(f"Updated guest: {email}\n")
            input("Press Enter to Continue\n")
            return
    print(f"Guest with email {email} not found.")
    input("Press Enter to Continue\n")


def delete_guest(email):
    """
    Deletes guest entry by searching for their email address.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    for idx, record in enumerate(records):
        if record["Email Address"] == email:
            row_number = idx + 2
            SHEET.worksheet(WORKSHEET).delete_rows(row_number)
            print(f"Deleted guest with email: {email}\n")
            input("Press Enter to Continue\n")
            return
    print(f"Guest with email {email} not found.\n")
    input("Press Enter to Continue\n")


def main():
    """
    Displays a menu and handles user input.
    """
    while True:
        clear()
        print("Hotel Management System\n")
        print("1. Add Guest")
        print("2. View All Guests")
        print("3. Search Guest by Email")
        print("4. Update Guest")
        print("5. Delete Guest")
        print("6. Exit\n")
        choice = input("Enter your choice:\n")
        if choice == "1":
            clear()
            while True:
                name = input("Enter guest name:\n")
                if not is_valid_name(name):
                    clear()
                    print(f"Invalid name - '{name}'\n")
                else:
                    clear()
                    break
            while True:
                phone = input("Enter phone number:\n")
                if not is_valid_phone(phone):
                    clear()
                    print(f"Invalid phone number - '{phone}'\n")
                else:
                    clear()
                    break
            while True:
                address = input("Enter address:\n")
                if not is_valid_address(address):
                    clear()
                    print(f"Invalid address - '{address}'\n")
                else:
                    clear()
                    break
            while True:
                email = input("Enter email:\n")
                if not is_valid_email(email):
                    clear()
                    print(f"Invalid Email Address - '{email}'\n")
                elif email_exists(email):
                    clear()
                    print(f"Email '{email}' already exists.\n")
                else:
                    clear()
                    break
            while True:
                room_class = input(
                    "Enter room class [Single, Double, Suite]:\n")
                if not is_valid_room_class(room_class):
                    clear()
                    print(f"Invalid Room class - '{room_class}'\n")
                else:
                    clear()
                    break
            while True:
                room_number = input("Enter room number:\n")
                if not is_valid_room_number(room_number):
                    clear()
                    print(f"Invalid Room Number - '{room_number}'\n")
                else:
                    clear()
                    break
            while True:
                amount_paid = input("Enter amount paid:\n")
                if not is_valid_amount_paid(amount_paid):
                    clear()
                    print(f"Invalid Amount Paid - '{amount_paid}'\n")
                else:
                    clear()
                    break
            add_guest(name, phone, address, email, room_class, room_number, amount_paid)  # noqa
        elif choice == "2":
            clear()
            view_all_guests()
        elif choice == "3":
            clear()
            email = input("Enter guest email to search:\n")
            search_guest_by_email(email)
            input("Press Enter to Continue\n")
        elif choice == "4":
            clear()
            email = input("Enter guest email to update:\n")
            guest = get_guest_record_by_email(email)
            if guest:
                data_to_update = {}
                # Example of updating name
                new_name = input(f"Enter new name or leave blank to keep '{guest['Name']}':\n")  # noqa
                if new_name:
                    data_to_update["Name"] = new_name
                update_guest(email, data_to_update)
        elif choice == "5":
            clear()
            email = input("Enter guest email to delete:\n")
            delete_guest(email)
        elif choice == "6":
            clear()
            print("Goodbye!")
            break
        else:
            clear()
            print("Invalid choice. Please try again.\n")
