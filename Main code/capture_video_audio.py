import cv2
import pyaudio
import wave
import threading

# Function to capture video
def video_capture():
    cap = cv2.VideoCapture(0)  # Open the default camera
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
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
video_thread = threading.Thread(target=video_capture)
audio_thread = threading.Thread(target=audio_capture)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()
