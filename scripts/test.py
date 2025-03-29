import qrcode

data = input("What data do you want put in your QR Code?\n")

img = qrcode.make(data)
img.save("output/test.png")
