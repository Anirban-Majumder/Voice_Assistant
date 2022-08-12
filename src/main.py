from ui import *
from utils import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal
)



class Worker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    print_txt = pyqtSignal(str)

    r = sr.Recognizer()
    engine=pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 130)
    engine.setProperty("voice", voices[0].id)


    def process(self):
        self.started.emit()

        statement = self.get_input()
        if statement!=None:
            statement = statement.lower()
        else:
            return

        # add preferences and alert /alarm /reminder via json file

        if "open youtube" in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            self.speak("youtube is open now")

        elif "open google" in statement and not ("and" in statement or "search" in statement):
            webbrowser.open_new_tab("https://www.google.com")
            self.speak("Google is open now")

        elif "open gmail" in statement:
            webbrowser.open_new_tab("https://www.gmail.com")
            self.speak("Google Mail open now")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com")
            self.speak("Here is stackoverflow")

        elif "open discord" in statement:
            webbrowser.open_new_tab("https://discord.com")
            self.speak("Here is Discord")

        elif "news" in statement:
            webbrowser.open_new_tab("https://www.google.com/search?q=latest+news")
            self.speak("Here are some News headlines, Happy reading")

        elif "search "  in statement or "google " in statement:
            statement = statement.replace("search ", "")
            statement = statement.replace("for ", "")
            statement = statement.replace("google ", "")
            statement = statement.replace(" ", "+")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + statement)

        elif "play " in statement:
            #play that song from  youtube
            statement = statement.replace("play ", "")
            self.print_txt.emit("Playing in youtube : " + statement)
            statement = statement.replace(" ", "+")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + statement)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=" + video_ids[0])

            # for playing in local music
        #    statement = statement.replace("play ","")
        #    song=0
        #    if "random" in statement or "music" in statement:
        #        songs_found=find_file(".mp3")
        #        song = random.choice(songs_found[1]) if songs_found[0]!=0 else 0
        #    else:
        #        songs_found=find_file(statement)
        #        song = songs_found[1][0] if songs_found[0]!=0 else 0
        #
        #    if song :
        #        self.print_txt.emit("playing "+song)
        #        open_file(song)
        #    else:
        #        self.speak("sorry, I could not find your song in Music or Downloads")

        elif "stop" in statement:
            statement=statement.replace("stop ","")
            stop(statement)
            self.speak(statement+" has been stopped.")

        #elif "kill yourself" in statement:
        #    self.speak("initiating self destruction in 5 seconds")
        #    i=5
        #    self.engine.setProperty("rate", 200)
        #    while(i):
        #        self.speak(i)
        #        time.sleep(0.1)
        #        i-=1
        #    self.engine.setProperty("rate", 130)
        #    self.speak(disrespect())

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
            self.speak("I am a Voice-Assitant version 1 point O your persoanl assistant. I am programmed to minor tasks like"
                  "opening youtube, google chrome, gmail and stackoverflow, predict time, take a photo, search google, predict weather"
                  "in different cities, get the latest news too!")

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            self.speak("I was built by Anirban Majumder.")

        else:
            self.speak("Sorry, I can not do that.")

        self.finished.emit()
        print("finished")


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



class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Assistant()
        self.ui.setupUi(self)
        self.ui.activate_button.clicked.connect(self.onClick)

        #self.speak("Loading your super AI personal assistant")
        #self.wishMe()


    def onClick(self):
        # starting thread
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # connecting signals
        self.thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.started.connect(self.updateUi)
        self.worker.print_txt.connect(self.updateOutput)
        self.worker.finished.connect(self.resetUi)

        self.thread.start()


    def keyPressEvent(self, event):
        #print(event.key())
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.eql()


    def updateOutput(self,text):
        print(text)
        if len(text)>30 and "\n" not in text:
            text=text[:30] + "\n" + text[30:]
        self.ui.output.setText(text)
        self.ui.output.repaint()


    def wishMe(self):
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            self.speak("Hello,Good Morning")
        elif hour>=12 and hour<18:
            self.speak("Hello,Good Afternoon")
        else:
            self.speak("Hello,Good Evening")


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




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec())
