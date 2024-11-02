from tkinter import *

#login page function

def login_window(root, title_font):
    login_window = Toplevel(root)
    login_window.title("LOGIN")
    login_window.geometry("1000x800")

    title = Label(login_window, text="Welcome to the login", font=title_font)
    title.pack()


    back_button = Button(login_window, text="Back", command=login_window.destroy)
    back_button.place(x=10, y=760)

    text = Text(root, width=20, height=2, bg="blue")
    text.pack()