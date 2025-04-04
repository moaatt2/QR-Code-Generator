import os
import qrcode


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
    data += "FN:John Doe\n"

    # Name
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2
    ## Format: N:Last Name;First Name;Middle Name;Prefix;Suffix
    data += "N:Doe;John;;;\n"

    # Note
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2

    # Photo
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.4

    # Revision
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.4

    # Sound
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.5

    # Telephone
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
    data += "TEL;TYPE=cell:(000) 000-0000\n"
    data += "TEL;TYPE=fax:(100) 000-0000\n"

    # Email
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
    data += "EMAIL;TYPE=work:john_doe@work.com\n"
    data += "EMAIL;TYPE=home:john_doe@example.com\n"

    # Calendar URI
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.3
    data += "CALURI:http://example.com/calendar/jdoe\n"

    # Birthday
    ## Docs: https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.5
    data += "BDAY:19900101\n"

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
