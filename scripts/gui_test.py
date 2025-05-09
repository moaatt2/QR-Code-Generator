import os
import re
import qrcode
import datetime as dt
import validators
import tkinter

window = tkinter.Tk()

window.title("QR Code Generator")

label = tkinter.Label(window, text="Enter the URL or text to encode:").pack()
window.mainloop()
