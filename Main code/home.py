from tkinter import Tk, Label, Button, font, PhotoImage
import login
import signup

# Function to refresh and redisplay the main window
def refresh_main_window(root):
    print("Refreshing Main Window")
    root.deiconify()  # Make the main window visible again
    root.update()     # Update to ensure visibility

# Function to open the login window and hide the main window
def open_login(root):
    print("Opening Login Window")
    root.withdraw()  # Hide the main window temporarily
    login.login_window(root, refresh_main_window)  # Open login window, passing refresh function

# Function to open the sign-up window and hide the main window
def open_signup(root):
    print("Opening Sign-Up Window")
    root.withdraw()  # Hide the main window temporarily
    signup.signup_window(root, refresh_main_window)  # Open sign-up window, passing refresh function

# Configure the main application window
root = Tk()
root.title("Remote Mentor Tool")
root.configure(background="grey")
root.geometry("1000x800")

# Define font for title and buttons
title_font = font.Font(family="Helvetica", size=16, weight="bold")

# Title label
title_label = Label(root, text="Shabodi Mentorship Software", bg="grey", font=title_font)
title_label.place(relx=0.5, y=50, anchor="center")

# Load and center the logo image
try:
    image_shabodi = PhotoImage(file="shabodi_logo.gif")
    img_label = Label(root, image=image_shabodi, bg="grey")
    img_label.place(relx=0.5, rely=0.3, anchor="center")
except Exception as e:
    print(f"Error loading image: {e}")

# Login button
login_button = Button(root, text="Log In", bg="grey", width=20, height=2, font=title_font, command=lambda: open_login(root))
login_button.place(relx=0.5, rely=0.55, anchor="center")

# Sign-Up button
signup_button = Button(root, text="Sign Up", bg="grey", width=20, height=2, font=title_font, command=lambda: open_signup(root))
signup_button.place(relx=0.5, rely=0.65, anchor="center")

# Start the main event loop
root.mainloop()
