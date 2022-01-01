import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import os
import subprocess


engine=pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 110)
engine.setProperty('voice', voices[1].id)



def get_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
            print("say")
            audio = r.listen(source)
    try:            
        print("processing............")
        text = r.recognize_google(audio,language='en-in')
        print (text)
        return text
    except  :
        print("failed")
        return None


def speak(text):
    engine.say(text)
    engine.runAndWait()


def process(statement):
    
    if 'open youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("youtube is open now")
        time.sleep(5)

    elif 'open google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google is open now")
        time.sleep(5)

    elif 'open gmail' in statement:
        webbrowser.open_new_tab("gmail.com")
        speak("Google Mail open now")
        time.sleep(5)

    elif 'open vlc' in statement:
       os.startfile('b.mp3')

    





if __name__=='__main__':


    while True:
        speak("welcome to the world")       



        a=input("Enter to continue")
        statement = get_input()
        if statement==None:
            break
        statement = statement.lower()
        process(statement)