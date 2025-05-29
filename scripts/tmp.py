import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

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

# Create container with scroll bar and display vCard
vCardContainer = ttk.Frame(notebook)
canvas = tk.Canvas(vCardContainer, highlightthickness=0)
scrollbar = ttk.Scrollbar(vCardContainer, orient="vertical", command=canvas.yview)
vCard = ttk.Frame(canvas)
vCard.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
vCardWindow = canvas.create_window((0, 0), window=vCard, anchor="nw")

# Ensure that the frame in the canvas takes up full width of the canvas.
def resize_inner_frame(event):
    canvas.itemconfigure(vCardWindow, width=event.width)
canvas.bind("<Configure>", resize_inner_frame)

# Layout the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add content to vCard Tab
for number in range(30):
    ttk.Label(vCard, text=f"Field {number}").grid(row=number, column=0, sticky="e", padx=5, pady=2)
    ttk.Entry(vCard).grid(row=number, column=1, sticky="ew", padx=5, pady=2)

# Recursively bind mousewheel to vCard and all child elements to enable scrolling
def bind_mousewheel_recursive(widget, func):
    widget.bind("<MouseWheel>", func)
    for child in widget.winfo_children():
        bind_mousewheel_recursive(child, func)
bind_mousewheel_recursive(vCard, lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(vCardContainer, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
