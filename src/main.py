from ui import *
from utils import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal
)


# load config
config = loadConfig()


class Worker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    print_txt = pyqtSignal(str)

    r = sr.Recognizer()
    engine=pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 150)
    engine.setProperty("voice", voices[0].id)


    def process(self):
        self.started.emit()

        statement = self.get_input()
        if statement!=None:
            statement = statement.lower()
        else:
            statement = ""

        # add preferences and alert /alarm /reminder via json file
        if "chrome" in statement or "browser" in statement or "firefox" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            statement = statement.replace("open ", "")
            self.speak(f"{statement} is open now")

        elif "open youtube" in statement and not ("and" in statement or "play" in statement):
            webbrowser.open_new_tab("https://www.youtube.com")
            self.speak("Youtube is open now")

        elif "open google" in statement and not ("and" in statement or "search" in statement):
            webbrowser.open_new_tab("https://www.google.com")
            self.speak("Google is open now")

        elif "open gmail" in statement:
            webbrowser.open_new_tab("https://www.gmail.com")
            self.speak("GMail open now")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com")
            self.speak("Here is stackoverflow")

        elif "open discord" in statement:
            webbrowser.open_new_tab("https://discord.com")
            self.speak("Here is Discord")

        elif "open spotify" in statement:
            webbrowser.open_new_tab("https://open.spotify.com/")
            self.speak("Here is Spotify")

        elif "news" in statement:
            webbrowser.open_new_tab("https://www.google.com/search?q=latest+news")
            self.speak("Here are some News headlines, Happy reading")

        elif "search "  in statement or "google " in statement:
            statement = statement.replace("search ", "")
            statement = statement.replace("for ", "")
            statement = statement.replace("google ", "")
            statement = statement.replace(" ", "+")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + statement)
            self.speak("Here are some results")

        elif "play" in statement and "video" in statement or "video" in statement:
            #play the viedo from  youtube
            statement = statement.replace("play ", "")
            play_youtube(statement)
            self.print_txt.emit("Playing in youtube : " + statement)

        elif "play " in statement:
            statement = statement.replace("play ", "")

            if config["music_player"] == "youtube":
                play_youtube(statement)
                self.print_txt.emit("Playing in youtube : " + statement)

            elif config["music_player"] == "spotify":
                pass
                #statement = statement.replace(" ", "%20")
                #html = urllib.request.urlopen("https://open.spotify.com/search/" + statement)
                #regex search id from row1 of html and play the song


            elif config["music_player"] == "local":
                song = play_local(statement)
                if song != None:
                    self.print_txt.emit("playing " + song)
                    open_file(song)
                else:
                    self.speak("sorry, I could not find your song in Music or Downloads")

        elif "stop" in statement:
            statement=statement.replace("stop ","")
            stop(statement)
            self.speak(statement+" has been stopped.")

        elif "roast me" in statement or "tell me a joke" in statement:
            self.speak(disrespect())

        elif "weather " in statement:
            statement=statement.replace("weather","")
            statement=statement.replace("in","")
            statement=statement.replace("check","")
            statement=statement.replace("today","")
            statement=statement.replace(" ","")
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            self.speak("Checking weather in "+statement)
            city_name=statement
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404" and statement!="":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                self.speak(" Temperature is " +
                      str(int(current_temperature-273)) +" degree celsius"+
                      "\n humidity is " +
                      str(current_humidiy) +" percent"+
                      "\n description  " +
                      str(weather_description))
            else:
                self.speak(" City Not Found,\nplease say weather in <your city name>")

        elif "commands" in statement or "help" in statement or "who are you" in statement or "what are you" in statement or "what can you do" in statement:
            self.speak("I am a Voice-Assistant. I am programmed to minor tasks like launching browser opening youtube,"
                    " gmail and stackoverflow, playing music, playing youtube videos, telling jokes,"
                    " checking weather in different cities, and get the latest news too!")

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            self.speak("I was built by Anirban Majumder.")

        else:
            self.speak("Sorry, I can not do that.")

        self.finished.emit()


    def get_input(self):
        with sr.Microphone() as source:
            self.print_txt.emit("listening....")
            audio = self.r.listen(source)
        try:
            self.print_txt.emit("processing...")
            text = self.r.recognize_google(audio,language="en-in")
            #text = r.recognize_sphinx(audio)
            self.print_txt.emit("\t\tWas your Query : "+text+"  ")
            return text
        except Exception as e :
            print(e)
            self.speak("Could not understand you.")
            return None


    def speak(self,text):
        self.print_txt.emit(text)
        self.engine.say(text)
        self.engine.runAndWait()


    def wishMe(self):
        self.started.emit()

        hour=datetime.datetime.now().hour
        if hour >= 0 and hour < 12:
            txt = "Hello, Good Morning"
        elif hour >= 12 and hour < 18:
            txt = "Hello, Good Afternoon"
        else:
            txt = "Hello, Good Evening"

        text = f"{txt}.\nHow may I help you?"
        self.speak(text)
        self.finished.emit()



class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Assistant()
        self.ui.setupUi(self)
        self.ui.activate_button.clicked.connect(self.onClick)
        #self.wishMe()


    def onClick(self):

        self.createThread()

        # connecting other signals
        self.thread.started.connect(self.worker.process)
        self.worker.started.connect(self.updateUi)
        self.worker.print_txt.connect(self.updateOutput)
        self.worker.finished.connect(self.resetUi)

        self.thread.start()


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.onClick()
        if key == Qt.Key_Escape:
            sys.exit()


    def updateOutput(self, text):
        print(text)
        if len(text)>30 and "\n" not in text:
            text=text[:30] + "\n" + text[30:]
        self.ui.output.setText(text)
        self.ui.output.repaint()


    def wishMe(self):

        self.createThread()

        # connecting other signals
        self.thread.started.connect(self.worker.wishMe)
        self.worker.print_txt.connect(self.updateOutput)
        self.worker.started.connect(lambda: self.ui.activate_button.setEnabled(False))
        self.worker.finished.connect(lambda: self.ui.activate_button.setEnabled(True))

        self.thread.start()


    def resetUi(self):
        self.ui.activate_button.setEnabled(True)
        self.ui.activate_button.setStyleSheet(self.ui.default)
        self.ui.activate_button.setText("Activate")
        self.ui.activate_button.repaint()
        self.ui.direct.setText("Activate to Start listening")
        self.ui.direct.repaint()


    def updateUi(self):
        self.ui.direct.setText(" ")
        self.ui.direct.repaint()
        self.ui.activate_button.setEnabled(False)
        self.ui.activate_button.setText("Activated")
        self.ui.activate_button.setStyleSheet("border: 2px solid #006494; border-radius: 100px; border-style: inset; background: qradialgradient(cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1, radius: 1.35, stop: 0 #fff, stop: 1 #006494);")
        self.ui.activate_button.repaint()


    def createThread(self):
        # starting thread
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # connecting cleanup signals
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec())
