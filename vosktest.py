import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import tkinter as tk
import threading

# Set the path to your Vosk model directory
model_path = "C:/Users/YOGENDRA/Desktop/VEdit/model"  # Update this with the actual path to the Vosk model

# Initialize the Vosk model
model = Model(model_path)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open microphone stream
stream = p.open(rate=16000, channels=1, format=pyaudio.paInt16,
                input=True, frames_per_buffer=4000)

recognizer = KaldiRecognizer(model, 16000)

# Function to continuously listen to the microphone and recognize speech
def listen_to_microphone(insert_text_func):
    print("Please say something:")

    while True:
        data = stream.read(4000)

        # If the recognizer has received enough audio to process
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()  # Get the result after recognition
            text = json.loads(result)['text']  # Parse the recognized text
            print(text)

            # Insert the recognized text into the Text widget
            insert_text_func(f"{text}\n")

            # If 'exit' is detected, break the loop
            if 'exit' in text:
                print("Exiting...")
                break

# Function that inserts text into the Text widget in the main thread
def insert_text(text):
    text_widget.insert(tk.END, text)
    text_widget.yview(tk.END)  # Scroll to the bottom to view the latest text

# Function to start the background task (called immediately when the window is created)
def start_background_task():
    # Create a new thread to listen to the microphone and update the GUI
    thread = threading.Thread(target=listen_to_microphone, args=(insert_text,), daemon=True)
    thread.start()

# Tkinter window setup
root = tk.Tk()
root.title("Speech Recognition with Tkinter")
root.geometry("400x300")

# Create a Text widget to display text
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(pady=20)

# Start the background task automatically when the window is opened
start_background_task()

# Start the Tkinter event loop
root.mainloop()
