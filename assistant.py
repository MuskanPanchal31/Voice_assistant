import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import logging
import webbrowser

logging.basicConfig(level=logging.INFO)

class VoiceAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Golden Project (Voice Assistant)")
        self.root.geometry("800x600")
        self.root.configure(background='#2b2b2b')

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg='#3498db')
        self.header_frame.pack(fill='x')

        self.title_label = tk.Label(self.header_frame, text="Voice Assistant", font=('Arial', 24), bg='#3498db', fg='white')
        self.title_label.pack(pady=20)

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.main_frame.pack(fill='both', expand=True)

        # Microphone Button
        self.microphone_button = tk.Button(self.main_frame, text="Tap to Speak", command=self.record_voice, bg='#4CAF50', fg='white', font=('Arial', 18))
        self.microphone_button.pack(pady=20)

        # Text Area
        self.text_area = tk.Text(self.main_frame, height=15, width=50, bg='#f7f7f7', fg='black', font=('Arial', 14))
        self.text_area.pack(pady=20)

        # Footer Frame
        self.footer_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.footer_frame.pack(fill='x')

        self.clear_button = tk.Button(self.footer_frame, text="Clear", command=self.clear_text, bg='#e74c3c', fg='white', font=('Arial', 14))
        self.clear_button.pack(side='left', fill='x', expand=True)

        self.exit_button = tk.Button(self.footer_frame, text="Exit", command=self.root.destroy, bg='#e74c3c', fg='white', font=('Arial', 14))
        self.exit_button.pack(side='left', fill='x', expand=True)

        self.speak = pyttsx3.init()
        self.voices = self.speak.getProperty('voices')
        self.speak.setProperty('voice', self.voices[1].id)

    def record_voice(self):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                self.text_area.insert(tk.END, command + "\n")
                self.process_command(command)
            except sr.UnknownValueError:
                logging.error("Speech recognition could not understand audio")
            except sr.RequestError as e:
                logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)            
     
    def process_command(self, command):
        if 'alexa' in command:
            command = command.replace('alexa', '')
        if 'play' in command:
            self.play_song(command)
        elif 'open' in command:
            self.open_app(command)
        elif 'time' in command:
            self.tell_time()
        elif 'wikipedia' in command:
            self.search_wikipedia(command)
        else:
            self.speak_result("I didn't understand that command.")

    def play_song(self, command):
        song = command.replace('play', '').strip()
        try:
            pywhatkit.playonyt(song)
            self.speak_result("Playing " + song)
        except Exception as e:
            logging.error("Error playing song: {0}".format(e))

    def open_app(self, command):
        app = command.replace('open', '').strip()
        try:
            if app == "google":
                webbrowser.open("https://www.google.com")
            elif app == "youtube":
                webbrowser.open("https://www.youtube.com")
            else:
                os.system(f"start {app}")
            self.speak_result("Opening " + app)
        except Exception as e:
            logging.error("Error opening app: {0}".format(e))

    def tell_time(self):
        try:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak_result("The current time is " + time)
        except Exception as e:
            logging.error("Error getting time: {0}".format(e))

    def search_wikipedia(self, command):
        query = command.replace('wikipedia', '').strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            self.speak_result(result)
        except Exception as e:
            logging.error("Error searching Wikipedia: {0}".format(e))

    def speak_result(self, text):
        self.speak.say(text)
        self.speak.runAndWait()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()