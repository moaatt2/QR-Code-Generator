import qrcode

img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("output/test.png")
