import tkinter as tk
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame

# Create primary frame to hold QR sidebar and content entry notebook
window = tk.Tk()
window.title("QR Code Generator")
window.geometry("400x400")
window. resizable(False, False)

# Create Main Frame to hold notebook and sidebar
main_frame = tk.Frame(window)
main_frame.pack(expand=True, fill="both")

# Create sidebar
sidebar = tk.Frame(main_frame, width=200)
sidebar.pack(side="right", fill="y")
ttk.Button(sidebar, text="Update QR Code").pack(side="bottom", fill="x")

# Create notebook
notebook_frame = tk.Frame(main_frame)
notebook_frame.pack(side="left", expand=True, fill="both")
notebook = ttk.Notebook(notebook_frame)

# Create Tabs to add to notebook
raw_data = ttk.Frame(notebook)
vCard = ScrolledFrame(notebook, autohide=False)

# Tell vCard's second column (with entries) to expand
vCard.columnconfigure(1, weight=1)

# Add content to vCard Tab
for number in range(30):
    ttk.Label(vCard, text=f"Field {number}").grid(row=number, column=0, sticky="e", padx=5, pady=2)
    ttk.Entry(vCard).grid(row=number, column=1, sticky="ew", padx=(0, 15), pady=2)

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCard.container, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
