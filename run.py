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
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

def email_exists(email):
    records = SHEET.worksheet(WORKSHEET).get_all_records()
    
    # Iterate through each record to check for the email
    for record in records:
        if record.get('Email Address') == email:
            return True
    
    return False

def is_valid_room_class(room_class):
    # You can define accepted room classes as per your requirements
    accepted_classes = {'single', 'double', 'suite'}
    # Convert the input room_class to lowercase and check against accepted_classes
    return room_class.lower() in accepted_classes

def is_valid_room_number(room_number):
    room_number_str = str(room_number)  # Ensure the room number is a string
    return room_number_str.isdigit() and int(room_number_str) > 0 # Check if room number is a digit

def is_valid_amount_paid(amount_paid):
    try:
        float_amount = float(amount_paid)
        return float_amount >= 0  # Ensure amount paid is a positive number
    except ValueError:
        return False



        

def add_guest(name, phone, address, email, room_class, room_number, amount_paid):
    """
    Adds a new guest entry to the spreadsheet.
    """
    guest_data = [name, phone, address, email, room_class, room_number, amount_paid]
    SHEET.worksheet(WORKSHEET).append_row(guest_data) 
    clear()
    print(f"Added guest: {name}\n")
    input("Press Enter to Continue\n")

def view_all_guests():
    """
    Fetches and prints all guest entries from the spreadsheet using PrettyTable.
    """
    rows = SHEET.worksheet(WORKSHEET).get_all_values()

    if not rows:
        print("No data available.")
        return
    # Create a PrettyTable instance
    table = PrettyTable()

    # Set the field names (headers) using the first row of data
    table.field_names = rows[0]

    # Add the remaining rows to the table
    for row in rows[1:]:  # Skip the header row
        table.add_row(row)

    # Print the table
    print(table)

    input("Press Enter to Continue\n")
    


def search_guest_by_email(email):
    """
    Search for a guest entry using their email address and display the result in a formatted table.
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()  # Fetch all rows as dictionaries
    for record in records:
        if record["Email Address"] == email:
            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = record.keys()  # Set table headers to the keys of the record
            table.add_row(record.values())  # Add the guest's information as a row
            
            print(table)  # Print the formatted table
            return record  # Return the record as found

    print("Guest not found.")
    return None


def get_guest_record_by_email(email):
    """
    Search for a guest record using their email address 
    """
    records = SHEET.worksheet(WORKSHEET).get_all_records()  # Fetch all rows as dictionaries
    for record in records:
        if record["Email Address"] == email:
            return record  # Return the record as found

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
            row_number = idx + 2  # Row number in Google Sheets (1-based)
            for key, value in data_to_update.items():
                col_index = list(record.keys()).index(key) + 1  # Get the column index
                SHEET.worksheet(WORKSHEET).update_cell(row_number, col_index, value)
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
            row_number = idx + 2  # Row number in Google Sheets (1-based)
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
                # Get name and validate
                name = input("Enter guest name: ")
                if not is_valid_name(name):
                    clear()
                    print(f"You have entered an Invalid name - '{name}'\n")

                else:
                    clear()
                    break  # Move to the next input if name is valid
            
            while True:
                # Get phone number and validate
                phone = input("Enter phone number: ")
                if not is_valid_phone(phone):
                    clear()
                    print(f"You have entered an Invalid phone number - '{phone}'\n")
                else:
                    clear()
                    break  # Move to the next input if phone is valid

            while True:
                # Get address and validate
                address = input("Enter address: ")
                if not is_valid_address(address):
                    clear()
                    print(f"You have entered an Invalid address - '{address}'\n")
                else:
                    clear()
                    break  # Finish if address is valid

            while True:
                # Get Email and validate
                email = input("Enter email: ")
                
                if not is_valid_email(email):
                    clear()
                    print(f"You have entered an Invalid Email Address - '{email}'\n")
                elif email_exists(email):
                    clear()
                    print(f"The email address '{email}' already exists. Please enter a different email.\n")
                else:
                    clear()
                    break  # Finish if email is valid and doesn't already exist

            while True:
                # Get Room class and validate
                room_class = input("Enter room class [Single, Double, Suite]: ")
                if not is_valid_room_class(room_class):
                    clear()
                    print(f"You have entered an Invalid Room class - '{room_class}'\n")
                else:
                    clear()
                    break  # Finish if Room class is valid

            while True:
                # Get Room Number and validate
                room_number = input("Enter room number: ")
                if not is_valid_room_number(room_number):
                    clear()
                    print(f"You have entered an Invalid Room Number - '{room_number}'\n")
                else:
                    clear()
                    break  # Finish if Room Number is valid

            while True:
                # Get Amount Paid and validate
                amount_paid = input("Enter amount paid: ")
                if not is_valid_amount_paid(amount_paid):
                    clear()
                    print(f"You have entered an Amount Paid - '{amount_paid}'\n")
                else:
                    clear()
                    break  # Finish if Amount Paid is valid
                
                
            add_guest(name, phone, address, email, room_class, room_number, amount_paid)

            
        elif choice == "2":
            clear()
            view_all_guests()
        
        elif choice == "3":
            clear()
            email = input("Enter guest email to search: ")
            guest = search_guest_by_email(email)
 
            input("Press Enter to Continue\n")

        
        elif choice == "4":
            clear()
            email = input("Enter guest email to update: ")
            guest = get_guest_record_by_email(email)
            clear()

            if guest:
                
                # Validate and update guest name
                while True:
                    print("Press Enter to keep the current value or type a new value to update.\n")
                    name = input(f"Name [{guest['Guest Name']}]: ") or guest['Guest Name']
                    if is_valid_name(name):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid name - '{name}'")

                
                # Validate and update phone number
                while True:
                    print("Press Enter to keep the current value or type a new value to update.\n")
                    phone = input(f"Phone Number [{guest['Phone Number']}]: ") or guest['Phone Number']
                    if is_valid_phone(phone):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid phone number - '{phone}'\n") 
                
                # Validate and update address
                while True:
                    print("Press Enter to keep the current value or type a new value to update.\n")
                    address = input(f"Address [{guest['Address']}]: ") or guest['Address']
                    if is_valid_address(address):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid address - '{address}'\n")
                
                # Validate and update room class
                while True:
                    print("Press Enter to keep the current value or type a new value to update.")
                    print("Choose  [Single, Double, Suite].\n")
                    room_class = input(f"Room Class [{guest['Class of Room Booked']}]: ") or guest['Class of Room Booked']
                    if is_valid_room_class(room_class):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid Room class - '{room_class}'\n")
                
                # Validate and update room number
                while True:
                    print("Press Enter to keep the current value or type a new value to update.\n")
                    room_number = input(f"Room Number [{guest['Room Number']}]: ") or guest['Room Number']
                    if is_valid_room_number(room_number):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Invalid Room Number - '{room_number}'\n")
                
                # Validate and update amount paid
                while True:
                    print("Press Enter to keep the current value or type a new value to update.\n")
                    amount_paid = input(f"Amount Paid [{guest['Amount Paid']}]: ") or guest['Amount Paid']
                    if is_valid_amount_paid(amount_paid):
                        clear()
                        break
                    else:
                        clear()
                        print(f"You have entered an Amount Paid - '{amount_paid}'\n")  

                # Prepare the updated data dictionary
                updated_data = {
                    "Guest Name": name,
                    "Phone Number": phone,
                    "Address": address,
                    "Class of Room Booked": room_class,
                    "Room Number": room_number,
                    "Amount Paid": amount_paid
                }
                
                # Update the guest record
                update_guest(email, updated_data)



        
        elif choice == "5":
            email = input("Enter guest email to delete: ")
            delete_guest(email)
        
        elif choice == "6":
            print("Exiting...\n")
            break
        
        else:
            print("Invalid choice, try again.\n")
 
# Start the program
clear()
main()