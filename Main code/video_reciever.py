import cv2
import socket
import struct
import pickle
import threading
import pyaudio

# Define server IP and ports for video and audio streams
SERVER_IP = '172.20.10.3'  # Replace with actual IP address of the sender
VIDEO_PORT = 9999
AUDIO_PORT = 9998  # Separate port for audio

# Audio stream settings
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Function to receive and display video feed from the secondary computer
def video_receiver():
    # Setup socket for video
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.connect((SERVER_IP, VIDEO_PORT))

    data = b""
    payload_size = struct.calcsize("L")  # Size of packed frame length

    while True:
        # Receive frame size
        while len(data) < payload_size:
            packet = video_socket.recv(4096)  # Adjust buffer size if needed
            if not packet:
                break
            data += packet
        if len(data) < payload_size:
            break

        # Unpack frame size and retrieve the frame data
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += video_socket.recv(4096)

        # Extract frame and display
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_socket.close()
    cv2.destroyAllWindows()

# Function to receive and play audio in real-time
def audio_receiver():
    # Setup socket for audio
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.connect((SERVER_IP, AUDIO_PORT))

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    try:
        while True:
            # Receive audio data
            audio_data = audio_socket.recv(CHUNK)
            if not audio_data:
                break
            # Play audio data in real-time
            stream.write(audio_data)
    finally:
        # Cleanup audio resources
        stream.stop_stream()
        stream.close()
        p.terminate()
        audio_socket.close()

# Run video and audio receivers in separate threads
video_thread = threading.Thread(target=video_receiver)
audio_thread = threading.Thread(target=audio_receiver)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()
