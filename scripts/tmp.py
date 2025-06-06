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
vCard = ScrolledFrame(notebook, autohide=False)

# Add Content to Raw Data Tab
label = tkinter.Label(raw_data, text="QR Code Data:")
label.config(font=("Arial", 10, "bold"))
label.pack(pady=5)
tkinter.Text(raw_data).pack(padx=10, pady=5, fill="both", expand=True)

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

# Email
tkinter.Label(vCard, text="Email Address:").grid(row=27, sticky="e")
tkinter.Entry(vCard).grid(row=27, column=1, sticky="ew", padx=(0, 15))

# Email Type
tkinter.Label(vCard, text="Email Type:").grid(row=28, sticky="e")
email_type = ttk.Combobox(vCard, values=email_types, state="readonly")
email_type.grid(row=28, column=1, sticky="ew", padx=(0, 15))

# Section End Separator
ttk.Separator(vCard, orient="horizontal").grid(row=29, columnspan=2, sticky="ew", pady=5)



######################################
### Add Filler To Ensure Scrolling ###
######################################

for i in range(30, 50):
    tkinter.Label(vCard, text="Suffix:").grid(row=i, sticky="e")
    tkinter.Entry(vCard).grid(row=i, column=1, sticky="ew", padx=(0, 15))


#################################
#### Add Sections to Notebook ###
#################################

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard.container, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")


#####################
### Event Binding ###
#####################

## Combobox Behaviour
boxes = [email_type]

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
