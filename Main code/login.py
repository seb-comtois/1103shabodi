from tkinter import Toplevel, Label, Entry, Button, messagebox

def login_window(root, refresh_main_window):
    print("Creating Login Window")
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
        password = password_entry.get()
        # Implement your user verification logic here
        if username == "user" and password == "pass":  # Placeholder logic
            messagebox.showinfo("Login Successful", "You have logged in successfully!")
            login_win.destroy()
            refresh_main_window(root)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    Button(login_win, text="Log In", command=verify_login, bg="grey", fg="black").pack(pady=20)
    Button(login_win, text="Back", command=lambda: [login_win.destroy(), refresh_main_window(root)], bg="grey", fg="black").place(x=10, y=260)
    
    login_win.protocol("WM_DELETE_WINDOW", lambda: [login_win.destroy(), refresh_main_window(root)])
