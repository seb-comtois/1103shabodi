from tkinter import Tk, Label, Button, font, PhotoImage
import login
import signup
import dashboard  # Ensure dashboard is imported

def refresh_main_window(root):
    print("Refreshing Main Window")
    root.deiconify()
    root.update()

def open_login(root):
    print("Opening Login Window")
    root.withdraw()
    login.login_window(root, refresh_main_window, open_dashboard)

def open_signup(root):
    print("Opening Sign-Up Window")
    root.withdraw()
    signup.signup_window(root, refresh_main_window)

def open_dashboard(root):
    root.withdraw()  # Hide the main window when opening the dashboard
    dashboard.open_dashboard(root, refresh_main_window)

root = Tk()
root.title("Remote Mentor Tool")
root.configure(background="grey")
root.geometry("1000x800")

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = Label(root, text="Shabodi Mentorship Software", bg="grey", font=title_font)
title_label.place(relx=0.5, y=50, anchor="center")

try:
    image_shabodi = PhotoImage(file="shabodi_logo.gif")
    img_label = Label(root, image=image_shabodi, bg="grey")
    img_label.place(relx=0.5, rely=0.3, anchor="center")
except Exception as e:
    print(f"Error loading image: {e}")

login_button = Button(root, text="Log In", bg="grey", width=20, height=2, font=title_font, command=lambda: open_login(root))
login_button.place(relx=0.5, rely=0.55, anchor="center")

signup_button = Button(root, text="Sign Up", bg="grey", width=20, height=2, font=title_font, command=lambda: open_signup(root))
signup_button.place(relx=0.5, rely=0.65, anchor="center")

root.mainloop()
