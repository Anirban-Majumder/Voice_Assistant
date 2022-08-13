from distutils.command.config import config
import os, sys, subprocess
import glob
import datetime
import random
import pyttsx3
import time
import psutil
import speech_recognition as sr
import webbrowser
import requests
import urllib.request
import re
import json
#for voice in voices:
#    print(voice, voice.id)


# load config
def loadConfig():
    with open("config.json", "r") as f:
        return json.load(f)

def stop(program):
    try:
        for pid in (process.pid for process in psutil.process_iter() if process.name().lower()==  program+".exe"):
            os.kill(pid,9)
            print(program+" has been stopped.")
    except SystemError:
        print(SystemError)

def find_file(*args):
    files=[]
    for file in args:
        print(file)
        file = file.replace(" ","*")
        # add path here TODO load paths from json
        path = os.path.join(os.path.expanduser("~"),"Music","*" + file + "*")
        path2 = os.path.join(os.path.expanduser("~"),"Downloads","*" + file + "*")

        # finding the files in the path
        files= files + glob.glob(path,recursive=True) + glob.glob(path2,recursive=True)

    return len(files), files

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def disrespect():
    roast=["You suck at this so much,that it is incomprehensible.",
            " Your mom would be proud.......of your dumbness",
            "I have a puppy that do this better than you"]
    return roast[random.randint(0,2)]

def play_youtube(statement):
    statement = statement.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + statement)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    webbrowser.open_new_tab("https://www.youtube.com/watch?v=" + video_ids[0])


def play_local(statement):
    song = None
    # choosing a random music file
    if "random" in statement or "music" in statement:
        print("ran")
        songs_found=find_file(".mp3", ".aac", ".wav", ".flac", ".m4a", ".opus")
        song = random.choice(songs_found[1]) if songs_found[0]!=0 else None
    else:
        songs_found=find_file(statement)
        song = songs_found[1][0] if songs_found[0]!=0 else None
    print(songs_found)
    return song
