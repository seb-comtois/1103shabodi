from tkinter import Toplevel, Label, Button
import socket
import struct
import pickle
import cv2
import threading

# Configure the server address and port for the secondary computer connection
SERVER_ADDRESS = '172.20.10.3'  # Replace with the IP of the secondary computer
SERVER_PORT = 9999

# Flag to control the video feed
stop_epoccam_feed = False

def open_dashboard(root, refresh_main_window):
    print("Opening Dashboard Window")
    dashboard_win = Toplevel(root)
    dashboard_win.title("Dashboard")
    dashboard_win.geometry("400x400")
    dashboard_win.configure(bg="#1A1A1A")

    Label(dashboard_win, text="Dashboard", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A").pack(pady=20)

    # Button to connect to the secondary computer
    Button(dashboard_win, text="Connect to Secondary Computer", bg="grey", fg="black", width=25, height=2,
           command=start_secondary_computer_stream_thread).pack(pady=10)

    # Button to connect to EpocCam
    Button(dashboard_win, text="Connect to EpocCam", bg="grey", fg="black", width=25, height=2,
           command=lambda: start_epoccam_stream_thread(dashboard_win, refresh_main_window, root)).pack(pady=10)

    # Back button to return to the main screen
    Button(dashboard_win, text="Back", command=lambda: [dashboard_win.destroy(), refresh_main_window(root)],
           bg="grey", fg="black").place(x=10, y=360)

    dashboard_win.protocol("WM_DELETE_WINDOW", lambda: [dashboard_win.destroy(), refresh_main_window(root)])

def start_secondary_computer_stream_thread():
    threading.Thread(target=receive_secondary_computer_stream, daemon=True).start()

def start_epoccam_stream_thread(dashboard_win, refresh_main_window, root):
    global stop_epoccam_feed
    stop_epoccam_feed = False  # Reset the flag to allow the video feed to start
    threading.Thread(target=receive_epoccam_stream, args=(dashboard_win, refresh_main_window, root), daemon=True).start()

def receive_secondary_computer_stream():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    except ConnectionRefusedError:
        print("Failed to connect to the secondary computer. Make sure 'server.py' is running on the secondary computer.")
        return

    data = b""
    payload_size = struct.calcsize("L")

    try:
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    return
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                packet = client_socket.recv(4096)
                if not packet:
                    return
                data += packet

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Secondary Computer Video", frame)

            if cv2.waitKey(1) == ord('q'):
                break

    finally:
        client_socket.close()
        cv2.destroyWindow("Secondary Computer Video")

def receive_epoccam_stream(dashboard_win, refresh_main_window, root):
    global stop_epoccam_feed
    epoccam_index = 1  # Force to use EpocCam on index 1

    # Open EpocCam feed
    epoccam_capture = cv2.VideoCapture(epoccam_index)
    if not epoccam_capture.isOpened():
        print("Could not open EpocCam on index 1. Ensure it is connected and recognized by your computer.")
        return

    # Create a back button in the Tkinter window to stop the feed
    back_button = Button(dashboard_win, text="Back", bg="grey", fg="black", command=lambda: stop_feed_and_return(dashboard_win, refresh_main_window, root))
    back_button.place(x=10, y=360)

    try:
        while not stop_epoccam_feed:
            ret, frame = epoccam_capture.read()
            if not ret:
                print("Failed to receive frame from EpocCam.")
                break

            cv2.imshow("EpocCam Video", frame)
            if cv2.waitKey(1) == ord('q') or stop_epoccam_feed:
                break

    finally:
        epoccam_capture.release()
        cv2.destroyWindow("EpocCam Video")

def stop_feed_and_return(dashboard_win, refresh_main_window, root):
    global stop_epoccam_feed
    stop_epoccam_feed = True  # Set the flag to stop the video feed
    dashboard_win.destroy()
    refresh_main_window(root)

# Run test_camera_indices directly when running dashboard.py
if __name__ == "__main__":
    # Directly attempt to open EpocCam on index 1 for testing
    receive_epoccam_stream()
