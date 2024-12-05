import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
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
    TextArea.insert(END, text)
    TextArea.yview(END)  # Scroll to the bottom to view the latest text

# Function to start the background task (called immediately when the window is created)
def start_background_task():
    # Create a new thread to listen to the microphone and update the GUI
    thread = threading.Thread(target=listen_to_microphone, args=(insert_text,), daemon=True)
    thread.start()


#python -m pip install SpeechRecognition[whisper-local]
def newFile():
    global file
    root.title("Untitled - VEdit")
    file = None
    TextArea.delete(1.0, END)


def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - VEdit")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()


def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            #Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - VEdit")
            print("File Saved")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp():
    root.destroy()

def cut():
    TextArea.event_generate(("<>"))

def copy():
    TextArea.event_generate(("<>"))

def paste():
    TextArea.event_generate(("<>"))

def about():
    showinfo("VEdit", "VEdit by ZoroJyiro")

if __name__ == '__main__':
    #Basic tkinter setup
    root = Tk()
    root.title("Untitled - VEdit")
    #root.wm_iconbitmap("1.ico")
    root.geometry("644x788")

    #Add TextArea
    TextArea = Text(root, font="lucida 13")
    file = None
    TextArea.pack(expand=True, fill=BOTH)

    # Lets create a menubar
    MenuBar = Menu(root)

    #File Menu Starts
    FileMenu = Menu(MenuBar, tearoff=0)
    # To open new file
    FileMenu.add_command(label="New", command=newFile)

    #To Open already existing file
    FileMenu.add_command(label="Open", command = openFile)

    # To save the current file

    FileMenu.add_command(label = "Save", command = saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label = "Exit", command = quitApp)
    MenuBar.add_cascade(label = "File", menu=FileMenu)
    # File Menu ends

    # Edit Menu Starts
    EditMenu = Menu(MenuBar, tearoff=0)
    #To give a feature of cut, copy and paste
    EditMenu.add_command(label = "Cut", command=cut)
    EditMenu.add_command(label = "Copy", command=copy)
    EditMenu.add_command(label = "Paste", command=paste)

    MenuBar.add_cascade(label="Edit", menu = EditMenu)

    # Edit Menu Ends

    # Help Menu Starts
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label = "About VEdit", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # Help Menu Ends

    root.config(menu=MenuBar)

    #Adding Scrollbar using rules from Tkinter lecture no 22
    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT,  fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    # # obtain audio from the microphone
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)
    # # recognize speech using whisper
    # try:
    #     entry = r.recognize_whisper(audio, language="english")
    #     print("Whisper thinks you said : " + entry)
    # except sr.UnknownValueError:
    #     print("Whisper could not understand audio")
    # except sr.RequestError as e:
    #     print(f"Could not request results from Whisper; {e}")

            
    # # Define a variable with some text
    # my_text_variable = entry



    # # Insert the variable's value into the Text widget
    # TextArea.insert(END, my_text_variable)
    start_background_task()


    root.mainloop()
