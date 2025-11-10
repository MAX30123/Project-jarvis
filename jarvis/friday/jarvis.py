import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import time



def speek(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("...")
        time.sleep(2)

        audio_text = r.listen(source)
        

        try:
            text = r.recognize_google(audio_text)
            return text.lower() 
        except sr.UnknownValueError:
            print("did not understand")
            return "" 
        except sr.RequestError as e:
            print("Ошибка google:", e)
            return ""

while True:

    command = listen()

    if "hello jarvis" in command:
        speek("hi sir, how are you today?")
    elif "jarvis how are you today":
        speek("good and how are you sir")
        if "good" in command or "fine" in command:
            speek("it's nice")
    elif "fine" in command or "good" in command:

        speek("this is good, want to start a new project?")
        if "yes" in command:
          
          speek("I creating a new project and can you say name of project")
          project_name1 = listen()
          project_name1 = project_name1 + ".py"
          open(project_name1, "w" , encoding="utf-8").write(print("the project was created"))

    elif "jarvis create project" in command:
          
          speek("I creating a new project and can you say name of project")
          project_name = listen()
          project_name = project_name + ".py"
          open(project_name,"w" , encoding="utf-8").write("print('the project was created')")

    elif "jarvis open google" in command:
        speek("Opening Google sir")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome")
    elif "jarvis open youtube" in command:
        speek("opening youtube sir")
        webbrowser.open('https://www.youtube.com')
    elif "jarvis open discord" in command:
        speek("opening discord sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Discord\app-1.0.9213\Discord")
    elif "jarvis open roblox" in command:
        speek("opening roblox sir")
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Roblox\Versions\version-f6dd34ecac7b4642\RobloxPlayerBeta")
    elif "jarvis open steam" in command:
        speek("opening steam sir")
        subprocess.Popen(r"C:\Program Files (x86)\Steam")
        


    
        
