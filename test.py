import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

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

print("Please say something:")

# Open a file to save the recognized speech
with open("recognized_text.txt", "w", encoding="utf-8") as file:
    while True:
        # Read audio data from the microphone
        data = stream.read(4000)

        # If the recognizer has received enough audio to process
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()  # Get the result after recognition
            text = json.loads(result)['text']  # Parse the recognized text
            print(text)

            # Write recognized text to the file
            file.write(text + "\n")

            # Check for 'exit' keyword to break the loop
            if 'exit' in text:
                print("Exiting...")
                break
