import time
import tkinter as tk
import threading
import speech_recognition as sr
#defining take command funtion for input
def takeCommand():
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
#  # A function that runs in the background (simulating a long task)
# def background_task():
#     for i in range(5):
#         time.sleep(1)
#         print(f"Background task running... {i+1} seconds")

    
#     print("Background task completed.")

# A function that updates the Tkinter window (like a button click event)
def start_background_task():
    # Start the background task in a new thread
    threading.Thread(target=takeCommand, daemon=True).start()

        


# Create the main window
root = tk.Tk()

my_text_variable = takeCommand()
# Create a Text widget (text area)
text_area = tk.Text(root, height=10, width=40)
text_area.pack()
# Insert the variable's value into the Text widget
text_area.insert(tk.END, my_text_variable)  # Correct use of tk.END
#  Add a button to start the background task
start_button = tk.Button(root, text="Start Task", command=start_background_task)
start_button.pack(pady=20)  
# Start the Tkinter event loop
root.mainloop()

