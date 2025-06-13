import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

# Create primary frame to hold QR sidebar and content entry notebook
window = tkinter.Tk()
window.title("QR Code Generator")
window.geometry("400x400")

# Load & resize image
raw_img = Image.open("output/vCardTest.png")
raw_img.thumbnail((400, 400), Image.LANCZOS)
img = ImageTk.PhotoImage(raw_img)

# Add image to window
panel = label = ttk.Label(window, image=img)
panel.pack(fill="both", expand="yes")

window.mainloop()
