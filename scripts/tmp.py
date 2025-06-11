import datetime as dt
import tkinter
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame

################
### Settings ###
################

emails = 1
email_types = [
    "",
    "Work",
    "Home",
]
email_layout = {}


########################
### Helper Functions ###
########################

# Blocks mousewheel event and forwards to scrolled frame for specified element
def block_and_forward_scroll(event):
    vCard.event_generate("<MouseWheel>", delta=event.delta)
    return "break"


# When a combobox is selected this avoids the selection highlight
# Also refreshes the blocking/forwarding of mousewheel events
def box_updated(event):
    event.widget.selection_clear()


#####################
### Tkinter Setup ###
#####################

# Create primary frame to hold QR sidebar and content entry notebook
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("400x400")
vCard = ScrolledFrame(window, autohide=False)
vCard.pack(fill="both", expand=True)

# Ensure that all scrolls of comboboxes in vCard dont affect the scrollbox
vCard.bind_class("TCombobox", "<MouseWheel>", lambda e: block_and_forward_scroll(e))

######################################
### Add Email Section to vCard Tab ###
######################################

vCard.columnconfigure(1, weight=1)

# Add Name Section Label
label = tkinter.Label(vCard, text="Email Address:")
label.config(font=("Arial", 11, "bold"))
label.grid(row=25, columnspan=2, pady=(5,0), sticky="ew")

# Add note about leaving blank
label = tkinter.Label(vCard, text="Leave this blank if you don't want to include an Email Address.")
label.config(font=("Arial", 7))
label.grid(row=26, columnspan=2, pady=(0,5), sticky="w")

# Add a frame to hold the email addresses, this way the expansion is easier to manage as just the frame needs moved.
emailFrame = ttk.Frame(vCard)
emailFrame.grid(row=27, columnspan=2, sticky="ew")
emailFrame.columnconfigure(1, weight=1)

# Email
address_label = tkinter.Label(emailFrame, text="Email Address:")
address_label.grid(row=1, sticky="e")
address_entry = tkinter.Entry(emailFrame)
address_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 15))

# Email Type
type_label = tkinter.Label(emailFrame, text="Email Type:")
type_label.grid(row=2, sticky="e")
email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
email_type.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 15))

# Add widgets to dict
email_layout[emails] = [
    address_label,
    address_entry,
    type_label,
    email_type,
]

# Bind email type to not highlight selection
email_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))


# Add Frame to hold add/remove buttons so they can each take half the space
button_frame = ttk.Frame(emailFrame)
button_frame.grid(row=4, columnspan=2, sticky="ew", pady=5, padx=(0,10))


# Function to add email field on request
def add_email():
    global emails

    # Add email field
    r = 1 + 2*emails
    address_label = tkinter.Label(emailFrame, text="Email Address:")
    address_label.grid(row=r, sticky="e")
    address_entry = tkinter.Entry(emailFrame)
    address_entry.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Add email type field
    r += 1
    type_label = tkinter.Label(emailFrame, text="Email Type:")
    type_label.grid(row=r, sticky="e")
    email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
    email_type.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Increment email count
    emails += 1

    # Add widgets to dict
    email_layout[emails] = [
        address_label,
        address_entry,
        type_label,
        email_type,
    ]

    # Bind selection event
    email_type.bind("<<ComboboxSelected>>", lambda e: box_updated(e))

    # Move button down
    button_frame.grid(row=r+1, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Enable delete button if more than one email field exists
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

    # Decrement Email Count
    emails -= 1

    # Move Button up
    r = 1 + 2*emails
    button_frame.grid(row=r, columnspan=2, sticky="ew", pady=5, padx=(5,15))

    # Disable delete button if only one email left
    if emails == 1:
        del_email_button.config(state=tkinter.DISABLED)


# Add Email Button
add_email_button = ttk.Button(button_frame, text="Add Email", command=add_email)
add_email_button.pack(side="left", expand=True, fill="x", padx=5)

# Del Email Button
del_email_button = ttk.Button(button_frame, text="Remove Email", command=del_email)
del_email_button.pack(side="right", expand=True, fill="x", padx=5)
del_email_button.config(state=tkinter.DISABLED)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=29, columnspan=2, sticky="ew", pady=5)


######################################
### Add Filler To Ensure Scrolling ###
######################################

for i in range(50, 70):
    tkinter.Label(vCard, text="Suffix:").grid(row=i, sticky="e")
    tkinter.Entry(vCard).grid(row=i, column=1, sticky="ew", padx=(0, 15))

window.mainloop()
