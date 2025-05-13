import os
import re
import qrcode
import datetime as dt
import validators
import tkinter
from tkinter import ttk

# Create primary frame to hold QR sidebar and content entry notebook
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("400x400")

# Create Main Frame to hold notebook and sidebar
main_frame = tkinter.Frame(window)
main_frame.pack(expand=True, fill="both")

# Create sidebar
sidebar = tkinter.Frame(main_frame, width=200)
sidebar.pack(side="right", fill="y")
ttk.Button(sidebar, text="Update QR Code").pack(side="bottom", fill="x")

# Create notebook
notebook_frame = tkinter.Frame(main_frame)
notebook_frame.pack(side="left", expand=True, fill="both")
notebook = ttk.Notebook(notebook_frame)

# Create Tabs to add to notebook
raw_data = ttk.Frame(notebook)
vCard = ttk.Frame(notebook)

# Add Content to Raw Data Tab
label = tkinter.Label(raw_data, text="QR Code Data:")
label.config(font=("Arial", 10, "bold"))
label.pack(pady=5)
tkinter.Text(raw_data).pack(padx=10, pady=5, fill="both", expand=True)

# Add content to vCard Tab
tkinter.Label(vCard, text="Display Name:").grid(row=0)
tkinter.Entry(vCard).grid(row=0, column=1)

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
