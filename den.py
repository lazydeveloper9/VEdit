import tkinter as tk
import threading
import speech_recognition as sr

# Function that generates the input (this could be any function that returns a string)
def generate_input():
 # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    # recognize speech using whisper
    try:
        entry = r.recognize_whisper(audio, language="english")
        print("Whisper thinks you said : " + entry)
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Whisper; {e}")
        return "None"
    return entry
# Function to simulate a background task that inserts text into the Text widget
def background_task(input_text,insert_text_func):
  # Simulate a delay or background processing
        # Insert the provided input text into the Text widget safely via the main thread
        # input_text = generate_input()   
        insert_text_func(f"{input_text}")

# Function that inserts text into the Text widget in the main thread
def insert_text(text):
    text_widget.insert(tk.END, text)
    text_widget.yview(tk.END)  # Scroll to the bottom to view the latest text

# Function to start the background task with input from another function
def start_background_task():
        # Get the input text from the generate_input function
        input_text = generate_input()
        # Create a new thread to run the background task
        threading.Thread(target=background_task, args=(input_text,insert_text), daemon=True).start()

# Tkinter window setup
root = tk.Tk()
root.title("Tkinter Text Insert with Threading")
root.geometry("400x300")

# Create a Text widget to display text
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(pady=20)

# Create a Button to start the background task
start_button = tk.Button(root, text="Start Task", command=start_background_task)
start_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
