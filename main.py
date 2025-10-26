import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

genai.configure(api_key="Write you api key here")  # Replace with your actual key
model = genai.GenerativeModel("gemini-2.0-flash")

# ===================== AI PROCESS FUNCTION =====================
def aiProcess(command):
    """
    Sends the user command to Gemini 2.0 and returns the AI response.
    """
    try:
        response = model.generate_content(
            f"You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. "
            f"Give short responses please.\nUser: {command}"
        )
       # return response.text.strip()
        answer=response.text.strip()
        print("Jarvis:",answer)
        return answer
    except Exception as e:
        return f"Sorry, I faced an issue: {e}"

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "show news" in c.lower():
        webbrowser.open("https://www.aajtak.in")

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
