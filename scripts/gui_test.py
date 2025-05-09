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

# Create notbook tabs
notebook_frame = tkinter.Frame(main_frame)
notebook_frame.pack(side="left", expand=True, fill="both")
notebook = ttk.Notebook(notebook_frame)

# Create Notebook Tabs
raw_data = ttk.Frame(notebook)
vCard = ttk.Frame(notebook)

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
