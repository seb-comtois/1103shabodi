import cv2
import socket
import struct
import pickle
import pyaudio

# Initialize socket for communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('server_ip_address', 9999))  # Replace with the server's IP and port

# Set up PyAudio for audio playback
audio_format = pyaudio.paInt16
channels = 1
rate = 44100
chunk = 1024
audio = pyaudio.PyAudio()
audio_stream = audio.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk)

try:
    while True:
        # Receive video data size and frame
        data_size = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]
        video_data = b""
        while len(video_data) < data_size:
            video_data += client_socket.recv(4096)
        frame = pickle.loads(video_data)
        cv2.imshow('Smart Glasses View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Receive audio data size and audio
        audio_size = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]
        audio_data = b""
        while len(audio_data) < audio_size:
            audio_data += client_socket.recv(4096)
        audio_stream.write(audio_data)  # Play audio data

finally:
    client_socket.close()
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()
    cv2.destroyAllWindows()
