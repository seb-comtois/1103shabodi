import cv2
import threading
import pyaudio
from tkinter import Toplevel, Label, Button
import webbrowser  # For opening the Zoom meeting link

# Audio settings for Iriun
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo
RATE = 48000  # 48000 Hz
CHUNK = 1024

def open_dashboard(root, refresh_main_window):
    print("Opening Dashboard Window")
    dashboard_win = Toplevel(root)
    dashboard_win.title("Dashboard")
    dashboard_win.geometry("400x400")
    dashboard_win.configure(bg="#1A1A1A")

    # Title label
    title_label = Label(dashboard_win, text="Connected Devices", font=("Helvetica", 16, "bold"), fg="white", bg="#1A1A1A")
    title_label.pack(pady=10)

    # Iriun Stream Button
    iriun_button = Button(dashboard_win, text="Iriun Stream", bg="grey", fg="black", command=start_iriun_stream_with_audio)
    iriun_button.pack(pady=5)

    # New Zoom Meeting button
    zoom_button = Button(dashboard_win, text="Host Zoom Meeting", bg="grey", fg="black", command=host_zoom_meeting)
    zoom_button.pack(pady=5)

    # Back button to return to the main screen
    back_button = Button(dashboard_win, text="Back", command=lambda: [dashboard_win.destroy(), refresh_main_window(root)], bg="grey", fg="black")
    back_button.place(x=10, y=360)

    dashboard_win.protocol("WM_DELETE_WINDOW", lambda: [dashboard_win.destroy(), refresh_main_window(root)])

def start_iriun_stream_with_audio():
    """Starts the Iriun video and audio stream."""
    iriun_audio_index = 0  # Using Device 1 as the Iriun microphone index
    
    # Highlighted change: Set camera index to 1
    threading.Thread(target=view_camera_and_audio_feed, args=(0, iriun_audio_index), daemon=True).start()

def view_camera_and_audio_feed(camera_index, audio_device_index=None):
    """Opens and displays a video feed for the specified camera index and captures audio from the specified audio device."""
    # Set up audio playback stream for output
    audio = pyaudio.PyAudio()

    # Set up audio input stream for Iriun microphone if specified
    if audio_device_index is not None:
        audio_stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True,
                                  input_device_index=audio_device_index, frames_per_buffer=CHUNK)
        
        # Output stream to play the audio through the computer's speakers
        output_stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    else:
        print("No audio device index specified for Iriun microphone.")
        audio_stream = None
        output_stream = None

    # Open video capture on the specified camera index
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Could not open camera index {camera_index}")
        return

    # Start video and audio loop
    try:
        while True:
            # Video feed
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to receive frame from camera index {camera_index}")
                break
            cv2.imshow(f"Camera Feed {camera_index}", frame)

            # Audio feed
            if audio_stream and output_stream:
                audio_data = audio_stream.read(CHUNK)
                output_stream.write(audio_data)  # Play audio data in real-time

            # Quit condition
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
        if output_stream:
            output_stream.stop_stream()
            output_stream.close()
        audio.terminate()

def host_zoom_meeting():
    """Opens the Zoom meeting host link in the default web browser."""
    zoom_host_link = "https://us04web.zoom.us/j/79614255182?pwd=LpSLx2wbdGP7gyXRua1DHBpfHgOPAN.1"
    webbrowser.open(zoom_host_link)
