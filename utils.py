import os, sys, subprocess
import glob
import datetime
import random
import pyttsx3
import time
import psutil
import speech_recognition as sr
import webbrowser


#for voice in voices:
#    print(voice, voice.id)




def stop(program):
    try:
        for pid in (process.pid for process in psutil.process_iter() if process.name().lower()==  program+".exe"):
            os.kill(pid,9)
            print(program+" has been stopped.")
    except SystemError:
        print(SystemError)

def find_file(file):
    file = file.replace(" ","*")
    path=os.path.join(os.path.expanduser("~"),"Music","*" + file + "*")
    path2=os.path.join(os.path.expanduser("~"),"Downloads","*" + file + "*")
    file=glob.glob(path,recursive=True) + glob.glob(path2,recursive=True)

    return len(file), file

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

