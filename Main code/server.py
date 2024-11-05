import cv2
import socket
import struct
import pickle
import pyaudio

# Setup for video capture
video_capture = cv2.VideoCapture(0)

# Setup for audio capture
audio_format = pyaudio.paInt16  # Audio format
channels = 1
rate = 44100
chunk = 512
audio = pyaudio.PyAudio()
audio_stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

# Setup socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))  # Use appropriate IP and port
server_socket.listen(5)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Capture and send video frame
        ret, frame = video_capture.read()
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        conn.sendall(message_size + data)

        # Capture and send audio data
        audio_data = audio_stream.read(chunk)
        audio_message_size = struct.pack("L", len(audio_data))
        conn.sendall(audio_message_size + audio_data)

finally:
    conn.close()
    video_capture.release()
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()
    server_socket.close()
