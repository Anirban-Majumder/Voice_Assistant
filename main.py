from ui import *
from PyQt5.QtWidgets import *
from utils import *
import requests

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Assistant()
        self.ui.setupUi(self)
        self.click()
        self.r = sr.Recognizer()
        self.engine=pyttsx3.init("sapi5")
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("rate", 130)
        self.engine.setProperty("voice", voices[1].id)
        #self.speak("Loading your super AI personal assistant Ani bot")
        #self.wishMe()

    def click(self):
        self.ui.activate_button.clicked.connect(self.eql)
  

        
    def eql(self):
        self.ui.direct.setText(" ")
        self.ui.direct.repaint()
        self.ui.activate_button.setStyleSheet(" border-radius: 100px;background:#00FF00")
        self.ui.activate_button.repaint()
        statement = self.get_input()
        if statement!=None:
            statement = statement.lower()
            self.process(statement)
        self.ui.activate_button.setStyleSheet(self.ui.default)
        self.ui.activate_button.repaint()
        self.ui.direct.setText("Activate to Start listening")
        self.ui.direct.repaint()

    def keyPressEvent(self, event):
        #print(event.key())
        
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.eql()  


    def get_input(self):

        with sr.Microphone() as source:
            self.printxt("listening....")
            audio = self.r.listen(source)
        try:            
            self.printxt("processing...")
            text = self.r.recognize_google(audio,language="en-in")
            #text = r.recognize_sphinx(audio)
            self.printxt ("\t\tWas your Query : "+text+"  ")
            return text
        except Exception as e :
            print(e)
            self.printxt("Could not understand you.")
            return None

    def speak(self,text):
        self.printxt(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def printxt(self,text):
        print(text)
        if len(text)>45 and "\n" not in text:
            text=text[:45] + '\n' + text[45:]
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

        
    def process(self,statement):
        
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
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            self.speak("Here is stackoverflow")
            
        elif "open discord" in statement:
            webbrowser.open_new_tab("https://discord.com")
            self.speak("Here is Discord")

        elif 'news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            self.speak('Here are some headlines from the Times of India, Happy reading')

        elif 'search '  in statement:
            statement = statement.replace("search ", "")
            statement = statement.replace("for ", "")
            statement = statement.replace("google ", "")
            statement = statement.replace(" ", "+")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + statement)


        elif "play " in statement:

            statement = statement.replace("play ","")
            song=0
            if "random" in statement or "music" in statement:
                songs_found=find_file(".mp3")
                song = random.choice(songs_found[1]) if songs_found[0]!=0 else 0
            else:
                songs_found=find_file(statement)
                song = songs_found[1][0] if songs_found[0]!=0 else 0
        
            if song :
            
                self.printxt("playing "+song)
                open_file(song)

            else:
                self.speak("sorry, I could not find your song in Music or Downloads")

        
        elif "stop music" in statement:
            stop("vlc")
            self.speak("vlc has been stopped.")
        
        elif "stop" in statement:
            statement=statement.replace("stop ","")
            stop(statement)
            self.speak(statement+" has been stopped.")

       
        elif "kill yourself" in statement:
            self.speak("initiating self destruction in 5 seconds")
            i=5
            self.engine.setProperty("rate", 200)
            while(i):       
                self.speak(i)
                time.sleep(0.1)
                i-=1
            self.engine.setProperty("rate", 130)
            self.speak(disrespect())

        elif "weather " in statement:
            statement=statement.replace("weather","")
            statement=statement.replace("in","")
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


        else:
            self.speak("Sorry, I can not do that.")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec())