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
window.geometry("400x700")

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


#####################################
### Add Name Section to vCard Tab ###
#####################################

vCard.grid_columnconfigure(1, weight=1)

# Add Name Section Label
label = tkinter.Label(vCard, text="Name Section:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=0, columnspan=2, pady=5, sticky="ew")

# Displayname
tkinter.Label(vCard, text="Display Name:").grid(row=1, sticky="e")
tkinter.Entry(vCard).grid(row=1, column=1, sticky="ew", padx=(0, 5))

# Prefix
tkinter.Label(vCard, text="Prefix:").grid(row=2, sticky="e")
tkinter.Entry(vCard).grid(row=2, column=1, sticky="ew", padx=(0, 5))

# First Name
tkinter.Label(vCard, text="First Name:").grid(row=3, sticky="e")
tkinter.Entry(vCard).grid(row=3, column=1, sticky="ew", padx=(0, 5))

# Middle Name
tkinter.Label(vCard, text="Middle Name:").grid(row=4, sticky="e")
tkinter.Entry(vCard).grid(row=4, column=1, sticky="ew", padx=(0, 5))

# Last Name
tkinter.Label(vCard, text="Last Name:").grid(row=5, sticky="e")
tkinter.Entry(vCard).grid(row=5, column=1, sticky="ew", padx=(0, 5))

# Suffix
tkinter.Label(vCard, text="Suffix:").grid(row=6, sticky="e")
tkinter.Entry(vCard).grid(row=6, column=1, sticky="ew", padx=(0, 5))

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=7, columnspan=2, sticky="ew", pady=5)

#####################################
### Add Note Section to vCard Tab ###
#####################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Notes Section:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=8, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="Leave this blank if you don't want to include a note.")
label.config(font=("Arial", 7))
label.grid(row=9, columnspan=2, pady=(0,5), sticky="w")

# Add Text Entry Section
tkinter.Text(vCard, height=3).grid(row=10, columnspan=2, padx=10, pady=5)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=11, columnspan=2, sticky="ew", pady=5)

###########################################
### Add Sound Link Section to vCard Tab ###
###########################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Sound Link:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=12, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="Leave this blank if you don't want to include a Sound Link.")
label.config(font=("Arial", 7))
label.grid(row=13, columnspan=2, pady=(0,5), sticky="w")

# Add Text Entry Section
tkinter.Entry(vCard).grid(row=14, columnspan=2, sticky="ew", pady=5)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=15, columnspan=2, sticky="ew", pady=5)


############################################
### Add Source Link Section to vCard Tab ###
############################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Source Link:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=16, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="This is intended to be a link to where an up to\ndate vCard file of this contact can be found.\nLeave this blank if you don't want to include a Source Link.")
label.config(font=("Arial", 7))
label.grid(row=17, columnspan=2, pady=(0,5), sticky="w")

# Add Text Entry Section
tkinter.Entry(vCard).grid(row=18, columnspan=2, sticky="ew", pady=5)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=19, columnspan=2, sticky="ew", pady=5)

#############################################
### Add Phone Number Section to vCard Tab ###
#############################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Phone Number:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=20, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="Leave this blank if you don't want to include a Phone Number.")
label.config(font=("Arial", 7))
label.grid(row=21, columnspan=2, pady=(0,5), sticky="w")

# Phone Number
tkinter.Label(vCard, text="Phone Number:").grid(row=22, sticky="e")
tkinter.Entry(vCard).grid(row=22, column=1, sticky="ew", padx=(0, 5))

# Phone Type
tkinter.Label(vCard, text="Phone Type:").grid(row=23, sticky="e")
ttk.Combobox(vCard, values=["Cell", "Home", "Work"], state="readonly").grid(row=23, column=1, sticky="ew", padx=(0, 5))

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=24, columnspan=2, sticky="ew", pady=5)

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
