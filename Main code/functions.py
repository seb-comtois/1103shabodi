from tkinter import *

def position_image(root, img):
    root.update_idletasks()  # Ensure that dimensions are updated

    # Get dimensions of the root window and the image
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_width = img.winfo_width()
    img_height = img.winfo_height()

    # Calculate x and y coordinates for centering
    x = (window_width - img_width) / 2
    y = (window_height - img_height) / 2
    
    img.place(x=x, y=y)  # Place the image at calculated center