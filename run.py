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

# INPUT VALIDATION FUNCTIONS


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

# FEATUREFUNCTIONS


def add_guest(name, phone, address, email):
    """
    Adds a new guest entry to the spreadsheet.
    """
    guest_data = [name, phone, address, email]
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


"""
Function to break long text
"""


def break_long_text(text, line_length=20):
    # Split the text into words
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the new word exceeds the desired line length
        if len(current_line) + len(word) + 1 > line_length:
            # If it does, start a new line
            lines.append(current_line)
            current_line = word  # Start the new line with the current word
        else:
            # If it does not, add the word to the current line
            if current_line:
                current_line += " "  # Add space before adding the new word
            current_line += word

    # Append the last line if there's any content left
    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


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
            add_guest(name, phone, address, email)
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
            clear()

            if guest:
                # Validate and update guest name
                while True:
                    print("""Press Enter to keep the current value or
                            type a new value to update.\n""")
                    name = input(f"Name [{guest['Guest Name']}]: ") or guest['Guest Name']
                    if is_valid_name(name):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid name - '{name}'")

                # Validate and update phone number
                while True:
                    print("""Press Enter to keep the current
                            value or type a new value to update.\n""")
                    phone = input(f"Phone Number [{guest['Phone Number']}]: \n") or guest['Phone Number']
                    if is_valid_phone(phone):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid phone number - '{phone}'\n")

                # Validate and update address
                while True:
                    print("""Press Enter to keep the current
                            value or type a new value to update.\n""")
                    address = input(f"Address [{guest['Address']}]: \n") or guest['Address']
                    if is_valid_address(address):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid address - '{address}'\n")

                # Prepare the updated data dictionary
                updated_data = {
                    "Guest Name": name,
                    "Phone Number": phone,
                    "Address": address
                }

                # Update the guest record
                update_guest(email, updated_data)
            else:
                clear()
                print(f"The Email Address you entered doesnt match any record - '{email}'\n")
                
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


# Start the program
clear()
main()
