import os
import qrcode
import datetime as dt
import validators


# Data for error correction levels
correction_mapping = {
    '1': ["L", qrcode.constants.ERROR_CORRECT_L,  "7% of data can be restored",],
    '2': ["M", qrcode.constants.ERROR_CORRECT_M, "15% of data can be restored",],
    '3': ["Q", qrcode.constants.ERROR_CORRECT_Q, "25% of data can be restored",],
    '4': ["H", qrcode.constants.ERROR_CORRECT_H, "30% of data can be restored",],
}


# terminal clearing utilty function
def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


# Helper function to get/confirm filename
def get_filename():
    while True:
        clearTerminal()
        filename = input("What do you want to name the file?\nExtensions will be stripped.\n\n")
        filename = filename.split(".")[0]
        clearTerminal()
        print(f"Are you sure that '{filename}.png' is the filename you want?")
        choice = input("(y/n): ")
        if choice.lower()[0] == "y":
            break
    
    return filename


# Create a function that creates a function that will 
def create_cleaner(*characters):
    def cleaner(text):
        for char in characters:
            text = text.replace(char, "")
        return text
    return cleaner


# Validate the Birthdate provide by the user - Ensure that it is in YYYY-MM-DD format
def validate_birthdate(test_date: str) -> bool:
    try:

        # convert date to date time object, if user provided invaid value it will throw a ValueError
        parsed_date = dt.datetime.strptime(test_date, "%Y-%m-%d")

        assert parsed_date.date() <= dt.date.today()

        # Return True if all checks pass
        return True

    except AssertionError:
        return False

    except ValueError:
        return False


# Variation of validate_birthdate that allows for empty strings
def validate_optional_birthdate(test_date: str) -> bool:
    if test_date == "":
        return True
    else:
        return validate_birthdate(test_date)


# Validate the URL provided by the user
def validate_url(url: str) -> bool:

    # Allow schemeless urls by adding a scheme if one is not provided
    if "://" not in url:
        url = "http://" + url

    # Check validity of URL
    if validators.url(url):
        return True
    else:
        return False


# Create a variant of the validate_url function that allows for empty strings
def validate_optional_url(url: str) -> bool:
    if url == "":
        return True
    else:
        return validate_url(url)


# Validate email provided by user
def validate_optional_email(email: str) -> bool:
    # Allow empty email
    if email == "":
        return True

    # Validators email check wrapper
    if validators.email(email):
        return True
    else:
        return False


# Helper function that asks a question and gives a confirmation
def question_with_confirmation(question,
                               confirmation,
                               cleaning_function=create_cleaner(";", ":"),
                               validation_function=None,
                               ):
    
    invalid = False
    while True:

        # Start Loop by Clearing Terminal
        clearTerminal()

        # Handle Restarting due to invalid input
        if invalid:
            print("Invalid response. Please try again.\n")
            invalid = False

        # Ask User for input
        response = input(question)
        if cleaning_function:
            response = cleaning_function(response)
        clearTerminal()

        # Handle Validation
        if validation_function:
            if not validation_function(response):
                invalid = True
                continue

        # Request Confirmation From User
        print(confirmation.format(response))
        choice = input("(y/n): ").lower()
        if len(choice) > 0:
            if choice[0] == "y":
                break
    return response


# Define a function to get  the error correction level
def get_correction_level():

    # Set indicator variable to check if input is valid
    invalid = False

    # Get and confirm error correction level
    while True:
        clearTerminal()

        # Handle last input invalid
        if invalid:
            print("Invalid selection. Please try again.\n")
            invalid = False

        # Ask user for input
        print("What level of error correction do you want?")
        for k, v in correction_mapping.items():
            print(f"\t{k}. Level {v[0]} - {v[2]}")
        correction_level = input(f"Make a selection (1-{max(correction_mapping.keys())}): ")
        clearTerminal()

        try:        
            # Check if input is what user desires
            correction_name = correction_mapping[correction_level][0]
            print(f"Are you sure that '{correction_name}' is the correction level you want?")
            choice = input("(y/n): ")
            if choice.lower()[0] == "y":
                break

        except KeyError:
            invalid = True
        
    return correction_mapping[correction_level][1]


# Main Loop for handling text data
def text_data():
    # Get and confirm data
    while True:
        clearTerminal()
        data = input("What data do you want put in your QR Code?\n")
        clearTerminal()
        print(f"Are you sure that '{data}' is the what should be in the QR Code?")
        choice = input("(y/n): ")
        if choice.lower()[0] == "y":
            break

    # Get filename
    filename = get_filename()

    # Get error correction level
    correction_level = get_correction_level()

    # Make and save qr code
    img = qrcode.make(data, error_correction=correction_level)
    img.save(f"output/{filename}.png")


# Main Loop for handling vCard data
def vcard():
    # Add Testing Data
    data = "BEGIN:VCARDD\n"
    data += "VERSION:4.0\n"

    # Formatted Name
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.1
    formatted_name = question_with_confirmation(
        "Please enter the name as you want it displayed:\n",
        "Are you sure that '{}' is the name you want displayed?"
    )
    data += f"FN:{formatted_name}\n"

    # Name
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2
    ## Format: N:Last Name;First Name;Middle Name;Prefix;Suffix
    last_name = question_with_confirmation(
        "Please enter the last name:\n",
        "Are you sure that '{}' is the last name you want?"        
    )
    first_name = question_with_confirmation(
        "Please enter the first name:\n",
        "Are you sure that '{}' is the first name you want?"
    )
    middle_name = question_with_confirmation(
        "Please enter the middle name:\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the middle name you want?"
    )
    prefix = question_with_confirmation(
        "Please enter the prefix:\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the prefix you want?"
    )
    suffix = question_with_confirmation(
        "Please enter the suffix:\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the suffix you want?"
    )
    data += f"N:{last_name};{first_name};{middle_name};{prefix};{suffix}\n"

    # Note
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2
    note = question_with_confirmation(
        "Please enter the note you want included.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the note you want?"
    )
    if note != "":
        data += f"NOTE:{note}.\n"

    # Revision
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.4
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    data += f"REV:{now}\n"

    # Sound
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.5
    sound_url = question_with_confirmation(
        "Please enter the URL of the sound file you want included.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the URL of the sound file you want?",
        cleaning_function=None,
        validation_function=validate_optional_url,
    )
    if sound_url != "":
        data += f"SOUND:{sound_url}\n"

    # Source
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.3
    source_url = question_with_confirmation(
        "Please enter the URL of the where an up to date version of this vCard found.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the URL of the up to date vCard file you want?",
        cleaning_function=None,
        validation_function=validate_optional_url,
    )
    if source_url != "":
        data += f"SOURCE:{source_url}\n"

    # Telephone
    # TODO: Add support for phone number types
    # TODO: Add support for multiple phone numbers
    # TODO: Add phone number verification
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
    ## Format: TEL;TYPE=type1,type2,...:number
    ## Types: home, work, cell, fax, pager, video, text, voice
    ## Example: TEL;TYPE=cell:(000) 000-0000
    phone_number = question_with_confirmation(
        "Please enter the phone number you want included.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the phone number you want?"
    )
    if phone_number != "":
        data += f"TEL:{phone_number}\n"

    # Email
    # TODO: Add support for multiple emails
    # TODO: Add email verification
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
    ## Format: EMAIL;TYPE=type,...:number
    ## Known Types: home, work
    # Example: EMAIL;TYPE=work:john_doe@work.com
    email = question_with_confirmation(
        "Please enter the email address you want included.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the email address you want?",
        validation_function=validate_optional_email,
    )
    if email != "":
        data += f"EMAIL:{email}\n"

    # Calendar URI
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.3
    calendar_url = question_with_confirmation(
        "Please enter the URL of the calendar you want included.\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the URL of the calendar you want?",
        cleaning_function=None,
        validation_function=validate_optional_url,
    )
    if calendar_url != "":
        data += f"CALURI:{calendar_url}\n"

    # Birthday
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.5
    ## Format: BDAY:YYYYMMDD
    birthday = question_with_confirmation(
        "Please enter the birthday you want included (in YYYY-MM-DD format).\nLeave it blank if you don't want to include one.\n",
        "Are you sure that '{}' is the birthday you want?",
        validation_function=validate_optional_birthdate,
    )
    if birthday != "":
        year, month, day = birthday.split("-")
        data += f"BDAY:{year}{month}{day}\n"

    data += "END:VCARD"

    # Get Filename
    # filename = get_filename()
    filename = "vCardTest"

    # Get Correction Level
    # correction_level = get_correction_level()
    correction_level = qrcode.constants.ERROR_CORRECT_L

    # Make and save qr code
    img = qrcode.make(data, error_correction=correction_level)
    img.save(f"output/{filename}.png")


# List of options and descriptions
options = {
    "1": [text_data, "Text Data"],
    "2": [vcard, "vCard"],
}


# Get and confirm error correction level
invalid = False
while True:
    clearTerminal()

    # Handle last input invalid
    if invalid:
        print("Invalid selection. Please try again.\n")
        invalid = False

    # Print selection options
    print("What kind of QR Code do you want to make?")
    for key, value in options.items():
        print(f"\t{key}. {value[1]}")

    # Get User input
    limit = max(map(int, options.keys()))
    selection = input(f"Make a selection (1-{limit}): ")
    clearTerminal()

    # Verify User Input
    try:        
        # Check if input is what user desires
        print(f"Please confirm that '{options[selection][1]}' is the QR Code Type you want?")
        choice = input("(y/n): ")
        if choice.lower()[0] == "y":
            break

    except KeyError:
        invalid = True

# Run selection option
options[selection][0]()
