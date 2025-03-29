import os
import qrcode


# terminal clearing utilty function
def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


# Get and confirm data
while True:
    data = input("What data do you want put in your QR Code?\n")
    clearTerminal()
    print(f"Are you sure that '{data}' is the what should be in the QR Code?")
    choice = input("(y/n): ")
    if choice.lower()[0] == "y":
        break

# Clear terminal after confirming data
clearTerminal()

# Get and confirm filename
while True:
    filename = input("What do you want to name the file?\n")
    clearTerminal()
    print(f"Are you sure that '{filename}.png' is the filename you want?")
    choice = input("(y/n): ")
    if choice.lower()[0] == "y":
        break

img = qrcode.make(data)
img.save(f"output/{filename}.png")
