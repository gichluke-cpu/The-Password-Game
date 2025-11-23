from PIL import Image, ImageTk
import tkinter as tk

def resize_background(event):
    global background_image, bg_image_tk
    
    # Resize image using PIL
    resized_image = bg_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(resized_image)

    canvas.delete("background")
    canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="background")

window = tk.Tk()
window.title("My Tkinter App")
window.geometry("800x600")

canvas = tk.Canvas(window, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Load image with Pillow
image_path = r"thequestionwall.jpg"
bg_image = Image.open(image_path)
bg_image_tk = ImageTk.PhotoImage(bg_image)

canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="background")

canvas.bind("<Configure>", resize_background)

window.mainloop()