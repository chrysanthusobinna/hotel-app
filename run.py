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
    return bool(name.strip()) and all(part.isalpha() or part.replace("-", "").isalpha()

def is_valid_phone(phone):
    # A simple regex for validating phone numbers (adjust as needed)
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone))

def is_valid_address(address):
    return bool(address.strip())  # Basic check: not empty

def is_valid_email(email):
    # Simple regex for validating email format
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

def is_valid_room_class(room_class):
    # You can define accepted room classes as per your requirements
    accepted_classes = {'Single', 'Double', 'Suite'}
    return room_class in accepted_classes

def is_valid_room_number(room_number):
    return room_number.isdigit()  # Check if room number is a digit

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

            while True:
                clear()
                name = input("Enter guest name: ")
                
                if is_valid_name(name):
                    break  # Exit the loop if the name is valid
                else:
                    print("Invalid name. Please try again.")
                    

            while True:
                clear()
                phone = input("Enter phone number: ")
                
                if is_valid_phone(phone):
                    break  # Exit the loop if the name is valid
                else:
                    print("Invalid phone number. Please enter a valid phone number.")


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
            print("Exiting...\n")
            break
        
        else:
            print("Invalid choice, try again.\n")
 
# Start the program
clear()
main()
 
 


   """

            while True:       
                clear()
                address = input("Enter address: ")
                if not is_valid_address(address):
                    print("Invalid address. Please enter a valid address.")
                    continue
            break

            while True:
                clear()
                email = input("Enter email: ")
                if not is_valid_email(email):
                    print("Invalid email. Please enter a valid email address.")
                    continue
            break
               
            while True:
                clear()
                room_class = input("Enter room class: ")
                if not is_valid_room_class(room_class):
                    print("Invalid room class. Please enter a valid room class (Single, Double, Suite).")
                    continue
            break
               
            while True:
                clear()
                room_number = input("Enter room number: ")
                if not is_valid_room_number(room_number):
                    print("Invalid room number. Please enter a valid room number.")
                    continue
            break
                
            while True:
                clear()
                amount_paid = input("Enter amount paid: ")
                if not is_valid_amount_paid(amount_paid):
                    print("Invalid amount. Please enter a valid amount paid.")
                    
            break
        """git