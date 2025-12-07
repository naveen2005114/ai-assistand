import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import webbrowser

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female/Male voice

# Initialize recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def open_software(software_name):
    """Open software or website"""
    software_name = software_name.lower()
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
    elif 'microsoft edge' in software_name:
        speak('Opening Microsoft Edge...')
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])
    elif 'youtube' in software_name or 'play' in software_name:
        speak('Opening YouTube...')
        query = software_name.replace('play', '').replace('youtube', '').strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe'])
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    else:
        speak(f"I couldn't find the software {software_name}")

def close_software(software_name):
    """Close software"""
    software_name = software_name.lower()
    if 'chrome' in software_name:
        speak('Closing Chrome...')
        os.system("taskkill /f /im chrome.exe")
    elif 'microsoft edge' in software_name:
        speak('Closing Microsoft Edge...')
        os.system("taskkill /f /im msedge.exe")
    elif 'notepad' in software_name:
        speak('Closing Notepad...')
        os.system("taskkill /f /im notepad.exe")
    elif 'calculator' in software_name:
        speak('Closing Calculator...')
        os.system("taskkill /f /im calculator.exe")
    else:
        speak(f"I couldn't find any open software named {software_name}")

def listen_for_wake_word():
    """Listen for wake word 'Jarvis'"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for wake word...")
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language='en_US').lower()
                if 'jarvis' in text:
                    speak('Hi Sir, How can I help you?')
                    return True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results; check your internet connection.")

def cmd():
    """Listen and execute user commands"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for your command...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='en_US').lower()
        print("Your message:", text)
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return False
    except sr.RequestError:
        speak("Could not request results; check your internet connection.")
        return False

    if 'stop' in text or 'exit' in text:
        speak("Stopping the program. Goodbye!")
        sys.exit()
    elif 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)
    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif 'who is god' in text:
        speak("Ajitheyyy Kadavuleyy")
    elif 'what is your name' in text:
        speak("My name is Jarvis, your Artificial Intelligence")
    else:
        speak("I can't perform that command yet.")

    return True

# Main loop
while True:
    if listen_for_wake_word():
        while True:
            if not cmd():
                continue
