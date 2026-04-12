#what's new in jarvis version 0.2? now jarvis know two languages: russian and english, 
#jarvis can wish you happy birthday and say what time and date today

#Imports
import webbrowser
import subprocess
import time
import datetime
import pyttsx3
import speech_recognition as sr

#Using pyttsx3 to create voice (tts)
def speek(text):
    engine = pyttsx3.init()#Initialization pyttsx3

    #properties of voice
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    engine.setProperty('volume', 1)

    engine.say(text)#Say the text
    engine.runAndWait()

#Using speech_recognition to listen to your voice (stt)
def listen():
    r = sr.Recognizer()#Initialization speech_recognition
    
    #Initialization microphone and listen 
    with sr.Microphone() as source:
        print("...")
        time.sleep(2)

        audio_text = r.listen(source)
        

        audio_text = r.listen(source)

        #Using try and expcept to know debug 
        try:
            text = r.recognize_google(audio_text)
            text = r.recognize_google(audio_text,language = "en-US")
            return text.lower() 
        except sr.UnknownValueError:
            pass
        try:
            text = r.recognize_google(audio_text,language = "ru-RU")
            return text.lower()
        #Debug if speech_recognition dont hear anything or didnt undrestand your voice
        except sr.UnknownValueError:
            print("did not understand")
            return "" 
        #Debug if google dont anwaser
        except sr.RequestError as e:
            print("Ошибка google:", e)
            return ""
#datetime        
date = datetime.date(2025, 11, 16) #set your birthday
date_today = datetime.date.today()
now = datetime.datetime.now()
time_str = now.strftime("%H:%M")

speek("Hi sir, I am jarvis your personal assistent. How can i help you today?")

#wish you happy birthday
if date == date_today:
 speek("Happy birthday sir")
 webbrowser.open('https://www.youtube.com/watch?v=0Xz1QAywzd0&list=RD0Xz1QAywzd0&start_radio=1')

while True:

    command = listen()

    if "hello jarvis" in command:
        speek("hi sir, how are you today?")

        requset = listen()

        if "fine" in requset or "good" in requset:
         speek("this is good, want to start a new project?")
         if "yes" in command:
          
          speek("I creating a new project and can you say name of project")
          project_name1 = listen()
          project_name1 = project_name1 + ".py"
          open(project_name1, "w" , encoding="utf-8").write(print("the project was created"))

    elif "jarvis how are you today":
        speek("good and how are you sir")
        if "good" in command or "fine" in command:
            speek("it's nice")

    elif "jarvis exit" in command:
        speek("Goodbye sir")
        break

    elif "jarvis" in command:
        speek("yes sir?")

    elif "jarvis create project" in command or "джарвис создай проект" in command:

          speek("I creating a new project and can you say name of project")
          project_name = listen()
          project_name = project_name + ".py"
          open(project_name,"w" , encoding="utf-8").write("print('the project was created')")


    #webbrowser

    elif "jarvis open youtube" in command or "джарвис открой ютуб" in command:
        speek("opening youtube sir")
        webbrowser.open('https://www.youtube.com')
        
    #subprocess
    elif "jarvis open discord" in command or "джарвис открой дискорд" in command:
        speek("opening discord sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Discord\app-1.0.9213\Discord")
    elif "jarvis open roblox" in command:
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Discord\app-1.0.9214\Discord.exe')
    elif "jarvis open roblox" in command or "джарвис открой роблокс" in command:
        speek("opening roblox sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Roblox\Versions\version-f6dd34ecac7b4642\RobloxPlayerBeta")
    elif "jarvis open steam" in command:
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Roblox\Versions\version-f6dd34ecac7b4642\RobloxPlayerBeta')
    elif "jarvis open steam" in command or "джарвис открой стим" in command:
        speek("opening steam sir")
        subprocess.Popen(r"C:\Program Files (x86)\Steam")
        
        subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
    elif "jarvis open google" in command or "джарвис открой гугл" in command:
        speek("Opening Google sir")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome")

    elif "jarvis open vscode" in command:
        speek("yes sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code")
        
    elif "jarvis open google" in command:
        speek("Opening Google sir")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome")

    #datetime
    elif "jarvis what time is it" in command or "который час" in command:
        speek(time_str)
    elif "what date is today" in command or "какое сегодня число" in command:
        speek(str(date_today))