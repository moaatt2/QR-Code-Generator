import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# Create primary frame to hold QR sidebar and content entry notebook
window = tk.Tk()
window.title("QR Code Generator")
window.geometry("400x400")

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

text = ScrolledText(notebook, state="disable", bg="#F0F0F0")
vCard = ttk.Frame(text)
text.window_create('1.0', window=vCard)

# Add content to vCard Tab
for number in range(30):
    l = tk.Label(vCard, text='Input:', bg='red')
    l.grid(row=number, column=0, sticky='we')
    l = tk.Label(vCard, text=number, bg='green')
    l.grid(row=number, column=1, sticky='we')

# Add Tabs to Notebook
notebook.add(raw_data, text="Raw Data")
notebook.add(text, text="vCard")

# Add notebook to UI
notebook.pack(expand=True, fill="both")

window.mainloop()
