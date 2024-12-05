import tkinter as tk
import threading
import speech_recognition as sr

# Function that generates the input (this will continuously listen to the microphone)
def generate_input(insert_text_func):
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        # recognize speech using Whisper
        try:
            text = r.recognize_whisper(audio, language="english")
            print("I think you said: " + text)
            # Insert recognized text into the Tkinter Text widget
            insert_text_func(text)
        except sr.UnknownValueError:
            print("I could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from API; {e}")
        
        # Exit condition based on the speech
        if 'exit' in text.lower():
            print("Exiting...")
            break

# Function to simulate a background task that inserts text into the Text widget
def background_task(insert_text_func):
    generate_input(insert_text_func)

# Function that inserts text into the Text widget in the main thread
def insert_text(text):
    text_widget.insert(tk.END, text + '\n')  # Insert text with newline for each new entry
    text_widget.yview(tk.END)  # Scroll to the bottom to view the latest text

# Tkinter window setup
root = tk.Tk()
root.title("Tkinter Speech Recognition")
root.geometry("400x300")

# Create a Text widget to display text
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(pady=20)

# Start the background task automatically when the window is opened
threading.Thread(target=background_task, args=(insert_text,), daemon=True).start()

# Start the Tkinter event loop
root.mainloop()
