# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Feature-by-Feature Testing

This section details the testing conducted on each feature of the project to ensure everything works as intended and provides a seamless experience for users.

### Project Display

## User Experience Testing

- **Usability Testing**: Conducted user tests with several individuals who interacted with the site and provided feedback. 
  - **Issues Encountered**: Users found the interface incompatible with mobile devices.
  - **Resolution**: Recommended accessing the site on PC devices for an optimal experience.
 
## Compatibility Testing

### Browser Compatibility

Tested the deployed project on various browsers to ensure consistent performance. Below are screenshots from Firefox, Chrome, and Edge (align screenshots side by side):

![Firefox](documentation/firefox-screenshot.png) ![Chrome](documentation/chrome-screenshot.png) ![Edge](documentation/edge-screenshot.png)

### Device Compatibility

Ensured functionality across various devices. Since this is a command-line project running on Node.js, it is more compatible with PC devices than mobile phones.

## Regression Testing

After implementing fixes or updates, I ensured that previous features and functionalities still work as intended. This prevented new changes from breaking existing features.

## Documentation and Logs

Maintained detailed records of testing procedures, results, and any bugs encountered, along with their resolutions, demonstrating a systematic approach to testing.

## User Feedback Incorporation

Collected user feedback from friends and peers and implemented improvements to enhance the user experience, particularly in validation messages and overall interface design in the command line.

## Code Validation

To ensure correct input and input types, I manually tested the code.

### Python

I used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files. Below is a screenshot of the validation result:

![Validation Screenshot](documentation/validation.png)

## Input Validation Testing

This section details the input validation functions implemented in the project to ensure that user inputs are correctly validated before proceeding.

### Name Validation (`is_valid_name`)

- **Purpose**: Ensures that the guest name contains only alphabetic characters and hyphens. The function trims any surrounding spaces and checks each part of the name for validity.
- **How it Works**: The input is split into words, and each word is validated to ensure that only alphabetic characters or hyphens are present.
- **Test**: Entered invalid characters like numbers or special characters (e.g., "John123" or "Mary!") and ensured the function rejected them, while valid inputs like "John-Doe" were accepted.
  
Screenshot:
![Name Validation Screenshot](documentation/name-validation.png)

### Phone Number Validation (`is_valid_phone`)

- **Purpose**: Validates the guest’s phone number, allowing optional spaces and ensuring the number is between 8 and 15 characters long. The phone number can also start with an optional `+` for international numbers.
- **How it Works**: The function uses a regular expression to ensure the phone number consists of digits and optional spaces, with a valid length range.
- **Test**: Tested invalid phone numbers like "12345" or "abcdef", which were rejected, while valid numbers like "09033526576" or "+1 234 567 8901" were accepted.
  
Screenshot:
![Phone Validation Screenshot](documentation/phone-validation.png)

### Address Validation (`is_valid_address`)

- **Purpose**: Ensures that the address field is not empty. This is a basic check to make sure users provide some input for the address.
- **How it Works**: The function trims the input and checks if there is any content remaining after trimming.
- **Test**: Entered empty strings or strings with just spaces, which were rejected, while valid addresses like "123 Main St." were accepted.
  
Screenshot:
![Address Validation Screenshot](documentation/address-validation.png)

### Email Validation (`is_valid_email`)

- **Purpose**: Ensures that the provided email address follows a valid format (e.g., name@domain.com). It uses a regular expression to match a valid email pattern.
- **How it Works**: The regular expression checks for a typical email format, including alphanumeric characters, dots, and other valid email characters.
- **Test**: Tested invalid emails like "name@domain" or "name.com", which were rejected, while valid emails like "john@example.com" were accepted.
  
Screenshot:
![Email Validation Screenshot](documentation/email-validation.png)

### Email Existence Check (`email_exists`)

- **Purpose**: Checks if the entered email address already exists in the system by querying the Google Sheets database.
- **How it Works**: The function retrieves all records from the worksheet and compares the input email to the existing email addresses.
- **Test**: Entered an email address that already existed in the system, and the function correctly identified it, preventing duplicate entries.
  
Screenshot:
![Email Exists Screenshot](documentation/email-exists.png)

## Defensive Programming

Defensive programming was employed throughout the application to ensure it handles incorrect inputs appropriately. One key area where this is implemented is around the **Main Menu**. When a user enters an invalid choice (such as a non-existent option in the menu), the application handles the error gracefully by:

- Displaying an error message indicating an invalid choice.
- Pausing to allow the user to read the message.
- Returning to the main menu, prompting the user to try again.

This ensures that the app remains user-friendly, even when unexpected inputs occur, and avoids crashes or unexpected behavior.

Below is a screenshot demonstrating this error handling in action:

![Defensive Programming Screenshot](documentation/defence-1.png)
![Defensive Programming Screenshot](documentation/defence-2.png)

---

## Bugs

No bugs were found during the testing process.
