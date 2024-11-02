# functions.py
from tkinter import *


#move image on homescreen
def position_image(root, img):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_width = img.winfo_width()
    img_height = img.winfo_height()

    x = (window_width - img_width) / 2
    y = (window_height - img_height) / 8
    
    img.place(x=x, y=y)


