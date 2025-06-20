import os
import re
import qrcode
import datetime as dt
import validators
import tkinter
import ttkbootstrap
from tkinter import ttk
from typing import Optional
from PIL import Image, ImageTk
from ttkbootstrap.scrolled import ScrolledFrame

################
### Settings ###
################

phones = 1
phone_types = [
    "",
    "text",
    "voice",
    "fax",
    "cell",
    "video",
    "pager",
    "textphone",
]
phone_layout = {}

emails = 1
email_types = [
    "",
    "Work",
    "Home",
]
email_layout = {}

panel_image = None

########################
### Helper Functions ###
########################

# Blocks mousewheel event and forwards to scrolled frame for specified element
def block_and_forward_scroll(event):
    vCard.event_generate("<MouseWheel>", delta=event.delta)
    return "break"


# When a combobox is selected this avoids the selection highlight
def box_updated(event):
    event.widget.selection_clear()


# Gets data from vCard tab and handles verification
def get_verify_vCard_data() -> Optional[str]:
    # Start version 4 vCard
    data = "BEGIN:VCARD\n"
    data += "VERSION:4.0\n"

    # Formatted Name
    display_name_clean = display_name.get().strip()
    data += f"FN:{display_name_clean}\n"

    # Full Name
    prefix_clean      = prefix.get().strip()
    first_name_clean  = first_name.get().strip()
    middle_name_clean = middle_name.get().strip()
    last_name_clean   = last_name.get().strip()
    suffix_clean      = suffix.get().strip()
    data += f"N:{last_name_clean};{first_name_clean};{middle_name_clean};{prefix_clean};{suffix_clean}\n"

    # Notes
    note_text = note_text_raw.get("1.0", "end").strip()
    if note_text != "":
        data += f"NOTE:{note_text}\n"

    # Sound Link
    sound_link_text = sound_link_entry.get().strip()
    if sound_link_text != "":
        data += f"SOUND:{sound_link_text}\n"

    # Source Link
    source_link_text = source_link_entry.get().strip()
    if source_link_text != "":
        data += f"SOURCE:{source_link_text}\n"

    # Phone numbers
    for i in phone_layout:
        number_text = phone_layout[i][1].get().strip()
        type_text = phone_layout[i][3].get().strip()

        if number_text != "":
            data += f"TEL;TYPE={type_text}:{number_text}\n"

    # Emails
    for i in email_layout:
        email_text = email_layout[i][1].get().strip()
        type_text = email_layout[i][3].get().strip()

        if email_text != "":
            if type_text != "":
                data += f"EMAIL;TYPE={type_text}:{email_text}\n"
            else:
                data += f"EMAIL:{email_text}\n"

    # Calendar URI
    calendar_link_text = calendar_link_raw.get().strip()
    if calendar_link_text != "":
        data += f"CALURI:{calendar_link_text}\n"

    # End vCard
    data += "END:VCARD"
    print()

    return data


# Gets data from the raw text box
#   Doesn't do any verification
def get_raw_data() -> str:
    return raw_data_text.get("1.0", "end").strip()


# Takes data, creates qr code, and updates sidebar
def generate_and_update_qr_code(data: str) -> None:
    # Use golbal variable to ensure that the image is stored outside the function's scope.
    global panel_image

    # Create QR Code
    raw_img = qrcode.make(data)
    raw_img = raw_img.resize((200, 200), Image.LANCZOS)

    # Update qr code in sidebar
    panel_image = ImageTk.PhotoImage(raw_img)
    panel.config(image=panel_image)


# Function to update the QR code based on user entered data.
def update_qr_code() -> None:

    # Check which tab is active
    active_tab = notebook.tab(notebook.select(), "text")

    # Handle Raw Data Tab
    if active_tab == "Raw Data":
        data = get_raw_data()
        generate_and_update_qr_code(data)

    # Handle vCard Tab
    elif active_tab == "vCard":
        data = get_verify_vCard_data()
        print(data)
        generate_and_update_qr_code(data)

    # Handle unknown tab
    else:
        raise ValueError(f"Unknown active tab: {active_tab}")


#####################
### Tkinter Setup ###
#####################

# Create primary frame to hold QR sidebar and content entry notebook
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("500x400")

# Create Main Frame to hold notebook and sidebar
main_frame = tkinter.Frame(window)
main_frame.pack(expand=True, fill="both")

# Create sidebar
sidebar = tkinter.Frame(main_frame, width=200)
sidebar.pack(side="right", fill="y")

# Create notebook
notebook_frame = tkinter.Frame(main_frame)
notebook_frame.pack(side="left", expand=True, fill="both")
notebook = ttk.Notebook(notebook_frame)

# Create Tabs to add to notebook
raw_data = ttk.Frame(notebook)
vCard = ScrolledFrame(notebook, autohide=False)

# Ensure that all scrolls of combobox and entry feilds in vCard only affect the scrollbox
vCard.bind_class("TCombobox", "<MouseWheel>", lambda e: block_and_forward_scroll(e))
vCard.bind_class("Entry", "<MouseWheel>", lambda e: block_and_forward_scroll(e))


#############################
### Image Sidebar Content ###
#############################

# Load & Resize Image
raw_img = Image.open("assets/placeholder.png") # Large image
raw_img = raw_img.resize((200, 200), Image.LANCZOS)
img = ImageTk.PhotoImage(raw_img)

# Add image to sidebar
panel = ttk.Label(sidebar, image=img)
panel.pack(fill="both", expand="yes", padx=5, pady=5)

ttk.Button(sidebar, text="Update QR Code", command=update_qr_code).pack(side="bottom", fill="x", padx=5, pady=5)


##########################
### Raw Data Tab Setup ###
##########################

# Label
label = tkinter.Label(raw_data, text="QR Code Data:")
label.config(font=("Arial", 10, "bold"))
label.pack(pady=5)

# Text Entry
raw_data_text = tkinter.Text(raw_data)
raw_data_text.pack(padx=10, pady=5, fill="both", expand=True)


#####################################
### Add Name Section to vCard Tab ###
#####################################

vCard.columnconfigure(1, weight=1)

# Add Name Section Label
label = tkinter.Label(vCard, text="Name Section:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=0, columnspan=2, pady=5, sticky="ew")

# Displayname
tkinter.Label(vCard, text="Display Name:").grid(row=1, sticky="e")
display_name = tkinter.Entry(vCard)
display_name.grid(row=1, column=1, sticky="ew", padx=(0, 15))

# Prefix
tkinter.Label(vCard, text="Prefix:").grid(row=2, sticky="e")
prefix = tkinter.Entry(vCard)
prefix.grid(row=2, column=1, sticky="ew", padx=(0, 15))

# First Name
tkinter.Label(vCard, text="First Name:").grid(row=3, sticky="e")
first_name = tkinter.Entry(vCard)
first_name.grid(row=3, column=1, sticky="ew", padx=(0, 15))

# Middle Name
tkinter.Label(vCard, text="Middle Name:").grid(row=4, sticky="e")
middle_name = tkinter.Entry(vCard)
middle_name.grid(row=4, column=1, sticky="ew", padx=(0, 15))

# Last Name
tkinter.Label(vCard, text="Last Name:").grid(row=5, sticky="e")
last_name = tkinter.Entry(vCard)
last_name.grid(row=5, column=1, sticky="ew", padx=(0, 15))

# Suffix
tkinter.Label(vCard, text="Suffix:").grid(row=6, sticky="e")
suffix = tkinter.Entry(vCard)
suffix.grid(row=6, column=1, sticky="ew", padx=(0, 15))

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
note_text_raw = tkinter.Text(vCard, height=3)
note_text_raw.grid(row=10, columnspan=2, padx=(5, 15), pady=5)

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
sound_link_entry = tkinter.Entry(vCard)
sound_link_entry.grid(row=14, columnspan=2, sticky="ew", pady=5, padx=(5, 15))

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
label = tkinter.Label(vCard, justify="left", text="This is intended to be a link to where an up to\ndate vCard file of this contact can be found.\nLeave this blank if you don't want to include a Source Link.")
label.config(font=("Arial", 7))
label.grid(row=17, columnspan=2, pady=(0,5), sticky="w")

# Add Text Entry Section
source_link_entry = tkinter.Entry(vCard)
source_link_entry.grid(row=18, columnspan=2, sticky="ew", pady=5, padx=(5, 15))

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

# Add a frame to hold the phone numbers & types
# Makes the expansion is easier to manage since no movement is needed
phoneFrame = ttk.Frame(vCard)
phoneFrame.grid(row=22, columnspan=2, sticky="ew")
phoneFrame.columnconfigure(1, weight=1)

# Phone Number
phone_label = tkinter.Label(phoneFrame, text="Phone Number:")
phone_label.grid(row=1, sticky="e", pady=5)
phone_entry = tkinter.Entry(phoneFrame)
phone_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 15))

# Phone Type
type_label = tkinter.Label(phoneFrame, text="Phone Type:")
type_label.grid(row=2, sticky="e", pady=5)
phone_type = ttk.Combobox(phoneFrame, values=phone_types, state="readonly")
phone_type.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 15))

# Bind phone type to not highlight selection
phone_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))

# Add widgets to layout
phone_layout[phones] = [
    phone_label,
    phone_entry,
    type_label,
    phone_type,
]


# Add Frame to hold add/remove buttons so they can each take half the space
phone_button_frame = ttk.Frame(phoneFrame)
phone_button_frame.grid(row=3, columnspan=2, sticky="ew", pady=5, padx=(5,15))


# Function to add phone field on request
def add_phone():
    global phones

    # Add phone number field
    r = 1 + 2*phones
    phone_label = tkinter.Label(phoneFrame, text="Phone Number:")
    phone_label.grid(row=r, sticky="e")
    phone_entry = tkinter.Entry(phoneFrame)
    phone_entry.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Add phone type field
    r += 1
    type_label = tkinter.Label(phoneFrame, text="Phone Type:")
    type_label.grid(row=r, sticky="e")
    phone_type = ttk.Combobox(phoneFrame, values=phone_types, state="readonly")
    phone_type.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Bind event to combobox to avoid selection highlight
    phone_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))

    # Increment phone count
    phones += 1

    # Add widgets to dict
    phone_layout[phones] = [
        phone_label,
        phone_entry,
        type_label,
        phone_type,
    ]

    # Move button down
    r += 1
    phone_button_frame.grid(row=r, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Enable delete button if more than one phone number field exists
    if phones > 1:
        del_phone_button.config(state=tkinter.NORMAL)


# Function to delete the last phone field
def del_phone():
    global phones

    # Remove last phone field
    for widget in phone_layout[phones]:
        widget.grid_forget()
        widget.destroy()

    # Remove items from phone layout
    del phone_layout[phones]

    # Decrement phone Count
    phones -= 1

    # Move Button frame up
    r = 1 + 2*phones
    phone_button_frame.grid(row=r, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Disable delete button if only one phone left
    if phones == 1:
        del_phone_button.config(state=tkinter.DISABLED)


# Add Phone Button
add_phone_button = ttk.Button(phone_button_frame, text="Add Number", command=add_phone)
add_phone_button.pack(side="left", expand=True, fill="x", padx=(0,5))

# Del Phone Button
del_phone_button = ttk.Button(phone_button_frame, text="Remove Number", command=del_phone)
del_phone_button.pack(side="right", expand=True, fill="x", padx=(5,0))
del_phone_button.config(state=tkinter.DISABLED)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=24, columnspan=2, sticky="ew", pady=5)

######################################
### Add Email Section to vCard Tab ###
######################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Email Address:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=25, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="Leave this blank if you don't want to include an Email Address.")
label.config(font=("Arial", 7))
label.grid(row=26, columnspan=2, pady=(0,5), sticky="w")

# Add a frame to hold the email addresses & types
# Makes the expansion is easier to manage since no movement is needed
emailFrame = ttk.Frame(vCard)
emailFrame.grid(row=27, columnspan=2, sticky="ew")
emailFrame.columnconfigure(1, weight=1)

# Email Address
email_label = tkinter.Label(emailFrame, text="Email Address:")
email_label.grid(row=1, sticky="e", pady=5)
email_entry = tkinter.Entry(emailFrame)
email_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 15))

# Email Type
type_label = tkinter.Label(emailFrame, text="Email Type:")
type_label.grid(row=2, sticky="e", pady=5)
email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
email_type.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 15))

# Bind email type to not highlight selection
email_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))

# Add widgets to layout
email_layout[emails] = [
    email_label,
    email_entry,
    type_label,
    email_type,
]


# Add Frame to hold add/remove buttons so they can each take half the space
email_button_frame = ttk.Frame(emailFrame)
email_button_frame.grid(row=3, columnspan=2, sticky="ew", pady=5, padx=(5,15))


# Function to add email field on request
def add_email():
    global emails

    # Add email number field
    r = 1 + 2*emails
    email_label = tkinter.Label(emailFrame, text="Email Address:")
    email_label.grid(row=r, sticky="e")
    email_entry = tkinter.Entry(emailFrame)
    email_entry.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Add email type field
    r += 1
    type_label = tkinter.Label(emailFrame, text="Email Type:")
    type_label.grid(row=r, sticky="e")
    email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
    email_type.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Bind event to combobox to avoid selection highlight
    email_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))

    # Increment email count
    emails += 1

    # Add widgets to dict
    email_layout[emails] = [
        email_label,
        email_entry,
        type_label,
        email_type,
    ]

    # Move button down
    r += 1
    email_button_frame.grid(row=r, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Enable delete button if more than one email number field exists
    if emails > 1:
        del_email_button.config(state=tkinter.NORMAL)


# Function to delete the last email field
def del_email():
    global emails

    # Remove last email field
    for widget in email_layout[emails]:
        widget.grid_forget()
        widget.destroy()

    # Remove items from email layout
    del email_layout[emails]

    # Decrement email count
    emails -= 1

    # Move Button frame up
    r = 1 + 2*emails
    email_button_frame.grid(row=r, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Disable delete button if only one email left
    if emails == 1:
        del_email_button.config(state=tkinter.DISABLED)


# Add Email Button
add_eamil_button = ttk.Button(email_button_frame, text="Add Email", command=add_email)
add_eamil_button.pack(side="left", expand=True, fill="x", padx=(0,5))

# Del Email Button
del_email_button = ttk.Button(email_button_frame, text="Remove Email", command=del_email)
del_email_button.pack(side="right", expand=True, fill="x", padx=(5,0))
del_email_button.config(state=tkinter.DISABLED)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=29, columnspan=2, sticky="ew", pady=5)

#############################################
### Add Calendar URI Section to vCard Tab ###
#############################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Calendar Link:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=30, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, justify="left", text="This is intended to be a link to an\nonline calendar showing your availability.\nLeave this blank if you don't want to include a Calendar Link.")
label.config(font=("Arial", 7))
label.grid(row=31, columnspan=2, pady=(0,5), sticky="w")

# Add Text Entry Section
calendar_link_raw = tkinter.Entry(vCard)
calendar_link_raw.grid(row=32, columnspan=2, sticky="ew", pady=5, padx=(5, 15))

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=33, columnspan=2, sticky="ew", pady=5)

#########################################
### Add Birthday Section to vCard Tab ###
##########################################

# Add Name Section Label
label = tkinter.Label(vCard, text="Birthday:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=34, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, justify="left", text="Leave this blank if you don't want to include your Birthday.\nDates should be formatted as YYYY-MM-DD.")
label.config(font=("Arial", 7))
label.grid(row=35, columnspan=2, pady=(0,5), sticky="w")

# Add Date Entry Section
date_entry = ttkbootstrap.DateEntry(vCard, dateformat="%Y-%m-%d")
date_entry.grid(row=36, columnspan=2, sticky="ew", pady=5, padx=(5, 15))
date_entry.entry.bind("<Key>", lambda e: "break")

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=37, columnspan=2, sticky="ew", pady=5)

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard.container, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")


#######################
### Start Main Loop ###
#######################

window.mainloop()
