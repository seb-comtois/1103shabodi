from tkinter import Toplevel, Label, Button

def open_dashboard(root, refresh_main_window):
    print("Opening Dashboard Window")
    dashboard_win = Toplevel(root)
    dashboard_win.title("Dashboard")
    dashboard_win.geometry("400x400")
    dashboard_win.configure(bg="#1A1A1A")

    Label(dashboard_win, text="Dashboard", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A").pack(pady=20)

    # Pair New Glasses Button
    Button(dashboard_win, text="Pair New Glasses", bg="grey", fg="black", width=20, height=2,
           command=lambda: open_pair_new_glasses(dashboard_win)).pack(pady=10)

    # Connect Past Glasses Button
    Button(dashboard_win, text="Connect Past Glasses", bg="grey", fg="black", width=20, height=2,
           command=lambda: open_connect_past_glasses(dashboard_win)).pack(pady=10)

    # Back button to return to the main screen
    Button(dashboard_win, text="Back", command=lambda: [dashboard_win.destroy(), refresh_main_window(root)], bg="grey", fg="black").place(x=10, y=360)

    dashboard_win.protocol("WM_DELETE_WINDOW", lambda: [dashboard_win.destroy(), refresh_main_window(root)])

def open_pair_new_glasses(dashboard_win):
    new_glasses_win = Toplevel(dashboard_win)
    new_glasses_win.title("Pair New Glasses")
    new_glasses_win.geometry("400x300")
    Label(new_glasses_win, text="Pairing New Glasses...", font=("Helvetica", 16), bg="#1A1A1A", fg="white").pack(pady=20)

def open_connect_past_glasses(dashboard_win):
    past_glasses_win = Toplevel(dashboard_win)
    past_glasses_win.title("Connect Past Glasses")
    past_glasses_win.geometry("400x300")
    Label(past_glasses_win, text="Connecting to Past Glasses...", font=("Helvetica", 16), bg="#1A1A1A", fg="white").pack(pady=20)
