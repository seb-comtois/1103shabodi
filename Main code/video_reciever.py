import cv2
import socket
import struct
import pickle
import threading
import pyaudio
import wave

# Function to receive and display video feed from the secondary computer
def video_receiver():
    # Setup socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.20.10.3', 9999))  # Replace with the actual IP address

    data = b""
    payload_size = struct.calcsize("L")  # Size of packed frame length

    while True:
        # Receive frame size
        while len(data) < payload_size:
            packet = client_socket.recv(4096)  # Adjust buffer size if needed
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
            data += client_socket.recv(4096)

        # Extract frame and display
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    client_socket.close()
    cv2.destroyAllWindows()

# Function to capture audio
def audio_capture():
    chunk = 1024  # Audio chunk size
    format = pyaudio.paInt16  # Format for recording
    channels = 2  # Number of audio channels
    rate = 44100  # Audio sample rate
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    print("Recording audio... Press Ctrl+C to stop.")
    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a file
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Run video and audio capture in separate threads
video_thread = threading.Thread(target=video_receiver)
audio_thread = threading.Thread(target=audio_capture)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()
