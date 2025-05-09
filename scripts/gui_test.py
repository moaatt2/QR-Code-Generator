import os
import re
import qrcode
import datetime as dt
import validators
import tkinter
from tkinter import ttk

# Create 
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("400x400")

notebook = ttk.Notebook(window)

raw_data = ttk.Frame(notebook)
vCard = ttk.Frame(notebook)

notebook.add(raw_data, text="Raw Data")
notebook.add(vCard, text="vCard")

notebook.pack(expand=True, fill="both")

code_image = tkinter.PhotoImage(file="output/test.png")
update_button = tkinter.Button(window, text="Update QR Code").pack()

window.mainloop()
