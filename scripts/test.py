import os
import qrcode


# terminal clearing utilty function
def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


# Get and confirm data
while True:
    clearTerminal()
    data = input("What data do you want put in your QR Code?\n")
    clearTerminal()
    print(f"Are you sure that '{data}' is the what should be in the QR Code?")
    choice = input("(y/n): ")
    if choice.lower()[0] == "y":
        break


# Get and confirm filename
while True:
    clearTerminal()
    filename = input("What do you want to name the file?\nExtensions will be stripped.\n\n")
    filename = filename.split(".")[0]
    clearTerminal()
    print(f"Are you sure that '{filename}.png' is the filename you want?")
    choice = input("(y/n): ")
    if choice.lower()[0] == "y":
        break


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
