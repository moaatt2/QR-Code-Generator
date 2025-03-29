import qrcode

data = input("What data do you want put in your QR Code?\n")

img = qrcode.make(data)
type(img)  # qrcode.image.pil.PilImage
img.save("output/test.png")
