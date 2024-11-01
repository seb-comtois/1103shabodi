# functions.py
from tkinter import *

def position_image(root, img):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_width = img.winfo_width()
    img_height = img.winfo_height()

    x = (window_width - img_width) / 2
    y = (window_height - img_height) / 8
    
    img.place(x=x, y=y)

def login_window(root, title_font):
    login_window = Toplevel(root)
    login_window.title("LOGIN")
    login_window.geometry("1000x800")

    title = Label(login_window, text="Welcome to the login", font=title_font)
    title.pack()


    back_button = Button(login_window, text="Back", command=login_window.destroy)
    back_button.place(x=10, y=760)
