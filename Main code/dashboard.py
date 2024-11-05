from tkinter import Toplevel, Label, Button, messagebox
import socket
import struct
import pickle
import cv2
import pyaudio
import threading

# Configure the server address and port (remote computer running server.py)
SERVER_ADDRESS = '192.168.1.136'  # Replace with the actual IP address of your friend's laptop
SERVER_PORT = 9999

def open_dashboard(root, refresh_main_window):
    print("Opening Dashboard Window")
    dashboard_win = Toplevel(root)
    dashboard_win.title("Dashboard")
    dashboard_win.geometry("400x400")
    dashboard_win.configure(bg="#1A1A1A")

    Label(dashboard_win, text="Dashboard", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A").pack(pady=20)

    # Button to connect to your friend's laptop
    Button(dashboard_win, text="Connect to Friend's Laptop", bg="grey", fg="black", width=25, height=2,
           command=start_video_audio_stream).pack(pady=10)

    # Back button to return to the main screen
    Button(dashboard_win, text="Back", command=lambda: [dashboard_win.destroy(), refresh_main_window(root)], bg="grey", fg="black").place(x=10, y=360)

    dashboard_win.protocol("WM_DELETE_WINDOW", lambda: [dashboard_win.destroy(), refresh_main_window(root)])

def start_video_audio_stream():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Set up audio playback
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

    try:
        while True:
            # Receive and display video frame
            video_message_size = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]
            video_data = b""
            while len(video_data) < video_message_size:
                video_data += client_socket.recv(4096)
            frame = pickle.loads(video_data)
            cv2.imshow('Smart Glasses Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Receive and play audio data
            audio_message_size = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]
            audio_data = b""
            while len(audio_data) < audio_message_size:
                audio_data += client_socket.recv(4096)
            stream.write(audio_data)
    
    finally:
        client_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        cv2.destroyAllWindows()
