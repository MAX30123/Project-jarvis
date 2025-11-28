import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import time
import datetime




#pyttsx3
def speek(text):
    engine = pyttsx3.init()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    engine.setProperty('volume', 1)

    engine.say(text)
    engine.runAndWait()
#speech_recognition
def listen():
    r = sr.Recognizer()
    

    with sr.Microphone() as source:
        print("...")


        audio_text = r.listen(source)
    
        try:
            text = r.recognize_google(audio_text,language = "en-US")
            return text.lower() 
        except sr.UnknownValueError:
            pass
        try:
            text = r.recognize_google(audio_text,language = "ru-RU")
            return text.lower 
        except sr.UnknownValueError:
            print("did not understand")
            return "" 
        except sr.RequestError as e:
            print("Ошибка google:", e)
            return ""
#datetime        
date = datetime.date(2025, 11, 16)
date_today = datetime.date.today()
now = datetime.datetime.now()
time_str = now.strftime("%H:%M")

speek("Hi sir, I am jarvis your personal assistent. How can i help you today?")

if date == date_today:
 speek("Happy birthday sir")
 webbrowser.open('https://www.youtube.com/watch?v=0Xz1QAywzd0&list=RD0Xz1QAywzd0&start_radio=1')

while True:

    command = listen()

    if "jarvis exit" in command:
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
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Discord\app-1.0.9214\Discord.exe')
    elif "jarvis open roblox" in command or "джарвис открой роблокс" in command:
        speek("opening roblox sir")
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Roblox\Versions\version-f6dd34ecac7b4642\RobloxPlayerBeta')
    elif "jarvis open steam" in command or "джарвис открой стим" in command:
        speek("opening steam sir")
        subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
    elif "jarvis open google" in command or "джарвис открой гугл" in command:
        speek("Opening Google sir")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome")

    elif "jarvis open vscode" in command:
        speek("yes sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code")

    #datetime
    elif "jarvis what time is it" in command or "который час" in command:
        speek(time_str)
    elif "what date is today" in command or "какое сегодня число" in command:
        speek(str(date_today))
