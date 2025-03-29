import qrcode


# Get and confirm data
while True:
    data = input("What data do you want put in your QR Code?\n")
    print()
    print(f"Are you sure that '{data}' is the what should be in the QR Code?")
    choice = input("(y/n): ")
    if choice.lower()[0] == "y":
        break


filename = input("What do you want to name the file?\n")
img = qrcode.make(data)
img.save(f"output/{filename}.png")
