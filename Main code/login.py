from tkinter import Toplevel, Label, Entry, Button, messagebox
import hashlib
from dashboard import open_dashboard

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_window(root, refresh_main_window, open_dashboard):
    print("Creating Login Window")  # Debug print to confirm function call
    login_win = Toplevel(root)
    login_win.title("Log In")
    login_win.geometry("400x300")
    login_win.configure(bg="#1A1A1A")

    Label(login_win, text="Log In", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A").pack(pady=10)
    
    Label(login_win, text="Username:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    username_entry = Entry(login_win, width=30)
    username_entry.pack()

    Label(login_win, text="Password:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    password_entry = Entry(login_win, width=30, show="*")
    password_entry.pack()

    def verify_login():
        username = username_entry.get()
        password = hash_password(password_entry.get())
        
        login_button.config(state="disabled")
        
        try:
            with open("data/users.txt", "r") as file:
                users = file.readlines()
            for user in users:
                saved_username, saved_password = user.strip().split(",")
                if saved_username == username and saved_password == password:
                    messagebox.showinfo("Login Successful", "You have logged in successfully!")
                    login_win.destroy()  # Close the login window
                    open_dashboard(root)  # Open the dashboard after login
                    return
            messagebox.showerror("Login Failed", "Incorrect username or password")
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
        
        login_button.config(state="normal")

    login_button = Button(login_win, text="Log In", command=verify_login, bg="grey", fg="black")
    login_button.pack(pady=20)
    Button(login_win, text="Back", command=lambda: [login_win.destroy(), refresh_main_window(root)], bg="grey", fg="black").place(x=10, y=260)
    
    login_win.protocol("WM_DELETE_WINDOW", lambda: [login_win.destroy(), refresh_main_window(root)])
