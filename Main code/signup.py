from tkinter import Toplevel, Label, Entry, Button, messagebox
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_password(password):
    if len(password) < 7:
        return False, "Password must be at least 7 characters long"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char in "!@#%^&*()_+" for char in password):
        return False, "Password must contain at least one special character"
    return True, ""

def signup_window(root, refresh_main_window):
    print("Creating Sign-Up Window")
    signup_win = Toplevel(root)
    signup_win.title("Sign Up")
    signup_win.geometry("400x400")
    signup_win.configure(bg="#1A1A1A")

    Label(signup_win, text="Sign Up", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A").pack(pady=10)

    Label(signup_win, text="Username:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    username_entry = Entry(signup_win, width=30)
    username_entry.pack()

    Label(signup_win, text="Password:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    password_entry = Entry(signup_win, width=30, show="*")
    password_entry.pack()

    Label(signup_win, text="Confirm Password:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    confirm_password_entry = Entry(signup_win, width=30, show="*")
    confirm_password_entry.pack()

    Label(signup_win, text="Manager Key:", fg="white", bg="#1A1A1A").pack(anchor="w", padx=50, pady=5)
    manager_key_entry = Entry(signup_win, width=30)
    manager_key_entry.pack()

    # Ensure the data directory and users.txt file exist
    os.makedirs("data", exist_ok=True)
    if not os.path.isfile("data/users.txt"):
        open("data/users.txt", "a").close()

    def verify_signup():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        manager_key = manager_key_entry.get()
        
        valid, message = is_valid_password(password)
        if not valid:
            messagebox.showerror("Error", message)
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if manager_key != "1234":
            messagebox.showerror("Error", "Invalid manager key")
            return

        hashed_password = hash_password(password)
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    saved_username, _ = line.strip().split(",")
                    if saved_username == username:
                        messagebox.showerror("Error", "Username already exists")
                        return
        except FileNotFoundError:
            pass

        # Save new user
        with open("data/users.txt", "a") as file:
            file.write(f"{username},{hashed_password}\n")
        
        messagebox.showinfo("Sign-Up Successful", "Your account has been created successfully!")
        signup_win.destroy()
        refresh_main_window(root)

    Button(signup_win, text="Sign Up", command=verify_signup, bg="grey", fg="black").pack(pady=20)
    Button(signup_win, text="Back", command=lambda: [signup_win.destroy(), refresh_main_window(root)], bg="grey", fg="black").place(x=10, y=360)
    
    signup_win.protocol("WM_DELETE_WINDOW", lambda: [signup_win.destroy(), refresh_main_window(root)])