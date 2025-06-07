import datetime as dt
import tkinter
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame

################
### Settings ###
################

email_types = [
    "",
    "Work",
    "Home",
]

#####################
### Tkinter Setup ###
#####################

# Create primary frame to hold QR sidebar and content entry notebook
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("400x400")
vCard = ScrolledFrame(window, autohide=False)
vCard.pack(fill="both", expand=True)

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


emailFrame = ttk.Frame(vCard)
emailFrame.grid(row=27, columnspan=2, sticky="ew")
emailFrame.columnconfigure(1, weight=1)

# Email
tkinter.Label(emailFrame, text="Email Address:").grid(row=1, sticky="e")
tkinter.Entry(emailFrame).grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 15))

# Email Type
tkinter.Label(emailFrame, text="Email Type:").grid(row=2, sticky="e")
email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
email_type.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 15))


emails = 1
combo_boxes = list()
combo_boxes.append(email_type)
email_add_button = ttk.Button(emailFrame, text="Add Add Additional Email")
email_add_button.grid(row=3, columnspan=2, sticky="ew", pady=5, padx=(5,15))
def add_email():
    global emails

    # Add email field
    r = 1 + 2*emails
    tkinter.Label(emailFrame, text="Email Address:").grid(row=r, sticky="e")
    tkinter.Entry(emailFrame).grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))

    # Add email type field
    r += 1
    tkinter.Label(emailFrame, text="Email Type:").grid(row=r, sticky="e")
    email_type = ttk.Combobox(emailFrame, values=email_types, state="readonly")
    email_type.grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 15))
    email_type.bind("<MouseWheel>", lambda e: block_and_forward_scroll(e))
    combo_boxes.append(email_type)

    # Increment email count
    emails += 1

    # Move button down
    email_add_button.grid(row=r+1, columnspan=2, sticky="ew", pady=5, padx=(5,15))

email_add_button.config(command=add_email)

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=29, columnspan=2, sticky="ew", pady=5)


######################################
### Add Filler To Ensure Scrolling ###
######################################

for i in range(30, 50):
    tkinter.Label(vCard, text="Suffix:").grid(row=i, sticky="e")
    tkinter.Entry(vCard).grid(row=i, column=1, sticky="ew", padx=(0, 15))


#####################
### Event Binding ###
#####################

## Combobox Behaviour
boxes = combo_boxes

def block_and_forward_scroll(event):
    vCard.event_generate("<MouseWheel>", delta=event.delta)
    return "break"


def box_updated(event):
    # Clear selection to avoid
    event.widget.selection_clear()

    # Allow scrolling but block updates
    for box in boxes:
        box.bind("<MouseWheel>", lambda e: block_and_forward_scroll(e))


for box in boxes:
    box.bind("<<ComboboxSelected>>", lambda e: box_updated(e))
    box.bind("<MouseWheel>", lambda e: block_and_forward_scroll(e))

window.mainloop()
