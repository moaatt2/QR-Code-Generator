import os
import re
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

# Data for phone number types
phone_types = {
    "1": ["text",      "text",      "text - the telephone number supports text messages."],
    "2": ["voice",     "voice",     "voice - a voice telephone number."],
    "3": ["fax",       "fax",       "fax - a facsimile telephone number."],
    "4": ["cell",      "cell",      "cell - a cellular or mobile telephone number."],
    "5": ["video",     "video",     "video - a video conferencing telephone number."],
    "6": ["pager",     "pager",     "pager - a paging device telephone number."],
    "7": ["textphone", "textphone", "textphone - a telecommunication device for people with hearing or speech difficulties."],
}

# Data for email types
email_types = {
    "1": ["work", "work", "work - An email address associated with work."],
    "2": ["home", "home", "home - An email address associated with personal life."],
    "3": ["", "Work/Home", "Work/Home - An email address associated with both work and personal life."],
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
def validate_email(email: str) -> bool:
    if validators.email(email):
        return True
    else:
        return False


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


# Validate phone number provided by user
def validate_phone_number(phone_number: str) -> bool:
    
    # Run regex match
    matches = re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone_number)
    return bool(matches)


# Validate phone number provided by user
def validate_optional_phone_number(phone_number: str) -> bool:
    # Allow empty phone number
    if phone_number == "":
        return True
    
    # Run regex match
    matches = re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone_number)
    return bool(matches)


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


# Helper function that provides options and requests confirmation
def options_with_confirmation(options, question, confirmation):

    invalid = False
    while True:

        # Start Loop by Clearing Terminal
        clearTerminal()

        # Handle Restarting due to invalid input
        if invalid:
            print("Invalid response. Please try again.\n")
            invalid = False

        # Print question and options
        print(question)
        for k, v in options.items():
            print(f"\t{k}. {v[2]}")

        # Get User input
        limit = max(map(int, options.keys()))
        selection = input(f"Make a selection (1-{limit}): ")
        clearTerminal()

        # Verify User Input
        try:        
            # Check if input is what user desires
            print(confirmation.format(options[selection][1]))
            choice = input("(y/n): ")
            if choice.lower()[0] == "y":
                break

        except KeyError:
            invalid = True

    return options[selection][0]

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
def text_data(debug=False):
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

    if debug:
        print("Debugging Information:")
        print()
        print(data)

    # Make and save qr code
    img = qrcode.make(data, error_correction=correction_level)
    img.save(f"output/{filename}.png")


# Main Loop for handling vCard data
def vcard(debug=False):
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
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
    ## Format: TEL;TYPE=type1,type2,...:number
    ## Types: home, work, cell, fax, pager, video, text, voice
    ## Example: TEL;TYPE=cell:(000) 000-0000
    phone_numbers_added = 0
    while True:
        # Determine what to ask user
        if phone_numbers_added == 0:
            question = "Would you like to add a phone number?"
        else:
            question = "Would you like to add another phone number?"
        
        # Ask question and get response
        clearTerminal()
        print(question)
        choice = input("(y/n): ").lower()

        # Handle Response
        if len(choice) > 0:
            if choice[0] == "y":
                phone_number = question_with_confirmation(
                    "Please enter the phone number you want included, in (XXX) XXX-XXXX format.",
                    "Are you sure that '{}' is the phone number you want?",
                    validation_function=validate_phone_number,
                )
                type = options_with_confirmation(
                    phone_types,
                    "What type of phone number is this?",
                    "Are you sure that '{}' is the type of phone number you want?",
                )
                data += f"TEL;TYPE={type}:{phone_number}\n"
                phone_numbers_added += 1
            else:
                break

    # Email
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
    ## Format: EMAIL;TYPE=type,...:number
    ## Known Types: home, work
    # Example: EMAIL;TYPE=work:john_doe@work.com
    emails_added = 0
    while True:
        # Determine what to ask user
        if emails_added == 0:
            question = "Would you like to add an email address?"
        else:
            question = "Would you like to add another email address?"
        
        # Ask question and get response
        clearTerminal()
        print(question)
        choice = input("(y/n): ").lower()

        # Handle Response
        if len(choice) > 0:
            if choice[0] == "y":
                email = question_with_confirmation(
                    "Please enter the email address you want included.\n",
                    "Are you sure that '{}' is the email address you want?",
                    validation_function=validate_email,
                )
                type = options_with_confirmation(
                    email_types,
                    "What type of email address is this?",
                    "Are you sure that '{}' is the type of email address you want?",
                )
                if type =="":
                    data += f"EMAIL:{email}\n"
                else:
                    data += f"EMAIL;TYPE={type}:{email}\n"
                emails_added += 1
            else:
                break


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

    if debug:
        print("Debugging Information:")
        print()
        print(data)

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
    "1": [text_data, "Text Data", "Text Data"],
    "2": [vcard,     "vCard",     "vCard"],
}

# Get QR code type choice and start primary function for given type
choice = options_with_confirmation(
    options,
    "What kind of QR Code do you want to make?",
    "Are you sure that '{}' is the QR Code Type you want?",
)
choice(debug=True)
