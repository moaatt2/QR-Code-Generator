import os
import qrcode


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

    # Error correction mapping
    correction_mapping = {
        '1': ["L", qrcode.constants.ERROR_CORRECT_L],
        '2': ["M", qrcode.constants.ERROR_CORRECT_M],
        '3': ["Q", qrcode.constants.ERROR_CORRECT_Q],
        '4': ["H", qrcode.constants.ERROR_CORRECT_H],
    }

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
        print("\t1. Level L - 7% of data can be restored")
        print("\t2. Level M - 15% of data can be restored")
        print("\t3. Level Q - 25% of data can be restored")
        print("\t4. Level H - 30% of data can be restored")
        correction_level = input("Make a selection (1-4): ")
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

    # Make and save qr code
    img = qrcode.make(data, error_correction=correction_mapping[correction_level][1])
    img.save(f"output/{filename}.png")


# Main Loop for handling vCard data
def vcard():
    print('TODO')


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
