import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import time
import datetime
import pygame
import pyautogui
import requests

#datetime        
date = datetime.date(2025, 11, 14)
date_today = datetime.date.today()
now = datetime.datetime.now()
time_str = now.strftime("%H:%M")

# GUI Setup
pygame.init()

font = pygame.font.SysFont(r'C:\code\image\Monocraft.ttc', 30) 

screen = pygame.display.set_mode((1500,1000))
pygame.display.set_caption("jarvisGUI")

user_text = "Listening..."
jarvis_text = "Connecting"

icon = pygame.image.load(r'C:\code\image\icon2.png')
pygame.display.set_icon(icon)
backg = pygame.image.load(r'C:\code\image\terminal.png')

#know weather now
def get_weather():
    API_KEY = "b3b1a603ceffddbe247b223101ec873d"
    City = "Tel Aviv"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={City}&appid={API_KEY}&units=metric&lang=ru"

    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        return {
            "temp": data["main"]["temp"],
            "feels": data["main"]["feels_like"],
            "desc": data["weather"][0]["description"]
        }
    else: 
        return None

# Function for drawing the screen (to avoid duplicating code)
def update_screen(screen, backg, font, weather):
    screen.blit(backg, (0, 0)) 

    text_user_surface = font.render('C:Users:user>' + user_text, True, 'white') 
    screen.blit(text_user_surface, (230, 250)) 

    Terminal = font.render('Jarvis [Version 0.25]  (Terminal)', True, 'white')
    screen.blit(Terminal, (300, 180))

    text_jarvis_surface = font.render("Jarvis: " + jarvis_text, True, 'white')
    screen.blit(text_jarvis_surface, (230, 300))

    if weather:

        text_temp = font.render(f"Температура: {weather['temp']}°C", True, 'white')
        screen.blit(text_temp, (700, 250))

        text_feels = font.render(f"Ощущается как: {weather['feels']}°C", True, 'white')
        screen.blit(text_feels, (700, 300))

        text_desc = font.render(f"{weather['desc']}", True, 'white')
        screen.blit(text_desc, (700, 350))

        if weather['temp'] > 21:
            ascii_sun = """                        |
                    .   |
                        |
          \    *        |     *    .  /
            \        *  |  .        /
         .    \     ___---___     /    .  
                \.--         --./     
     ~-_    *  ./               \.   *   _-~
        ~-_   /                   \   _-~     *
   *       ~-/                     \-~        
     .      |                       |      .
         * |                         | *     
-----------|                         |-----------
  .        |                         |        .    
        *   |                       | *
           _-\                     /-_    *
     .  _-~ . \                   /   ~-_     
     _-~       `\               /'*      ~-_  
    ~           /`--___   ___--'\           ~
           *  /        ---     .  \   jgs
            /     *     |           \\
          /             |   *         \\
                     .  |        .
                        |
                        |"""

            y = 400  
            for line in ascii_sun.splitlines():
                text_surf = font.render(line, True, 'white')
                screen.blit(text_surf, (700, y))
                y += 15

        elif weather['temp'] < 20:
            ascii_clouds = """          .-~~~-.
  .- ~ ~-(       )_ _
 /                     ~ -.
|                           \\
 \\                         .'
   ~- . _____________ . -~    """

            y = 400  
            for line in ascii_clouds.splitlines():
                text_surf1 = font.render(line, True, 'white')
                screen.blit(text_surf1, (700, y))
                y += 30

    pygame.display.update()

#pyttsx3
def speek(text):
    global jarvis_text 
    jarvis_text = text 
    
    update_screen(screen, backg, font, weather)

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

#speech_recognition
def listen():
    r = sr.Recognizer()

    r.pause_threshold = 0.7

    with sr.Microphone() as source:        
        global jarvis_text
        jarvis_text = "Online..."

        r.adjust_for_ambient_noise(source, duration=1)

        global user_text
        user_text = "Listening..." 
        update_screen(screen, backg, font,weather)
        
        try:
            audio_text = r.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return ""
    
        try:
            text = r.recognize_google(audio_text, language="en-US")
            return text.lower()
        except sr.UnknownValueError:
            pass
        
        try:
            text = r.recognize_google(audio_text, language="ru-RU")
            return text.lower() 
        except sr.UnknownValueError:
            print("did not understand")
            return ""
        except sr.RequestError as e:
            print("Ошибка google:", e)
            return ""
        
weather = None

speek("Connecting")

#if you know date of happy brirthday you can add your date
if date == date_today:
    speek("Happy birthday sir")
    webbrowser.open('https://www.youtube.com/watch?v=0Xz1QAywzd0&list=RD0Xz1QAywzd0&start_radio=1')


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    try:
        command = listen()

        if command:
            user_text = command

        if "jarvis sleep" in command:
            speek("Goodbye sir")
            running = False

        elif "jarvis create project" in command or "джарвис создай проект" in command:
            speek("I creating a new project and can you say name of project")
            project_name = listen()

            user_text = project_name

            if project_name:
                filename = project_name + ".py"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("print('the project was created')")
                speek(f"Project {project_name} created")

        #webbrowser
        elif "jarvis open youtube" in command or "джарвис открой ютуб" in command:
            speek("opening youtube sir")
            webbrowser.open('https://www.youtube.com')
        
        #subprocess
        elif "jarvis open discord" in command or "джарвис открой дискорд" in command:
            speek("opening discord sir")
            subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Discord\Update.exe --processStart Discord.exe')
        
        elif "jarvis open roblox" in command or "джарвис открой роблокс" in command:
            speek("opening roblox sir")
            subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Roblox\Versions\version-f6dd34ecac7b4642\RobloxPlayerBeta.exe')
        
        elif "jarvis open steam" in command or "джарвис открой стим" in command:
            speek("opening steam sir")
            subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
        
        elif "jarvis open google" in command or "джарвис открой гугл" in command:
            speek("Opening Google sir")
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        elif "jarvis open vs code" in command:
            speek("yes sir")
            subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code.exe")

        #datetime
        elif "jarvis what time is it" in command or "который час" in command:
            speek(time_str)

        elif "jarvis what date is today" in command or "какое сегодня число" in command:
            speek(str(date_today))

        #pyautogui

        elif "volume up" in command or "увеличь громкость" in command:
            pyautogui.press("volumeup")
            speek("volume increase")

        elif "volume down" in command or "уменьши громкость" in command:
            pyautogui.press("volumedown")
            speek("volume reduced")

        elif "volume mute" in command or "отключи звука" in command:
            pyautogui.press("volumemute")
            speek("turn off volume")

        elif "jarvis create screenshot" in command or "Джарвис создает скриншот" in command:
            speek("creating screenshot")
            screenShot = pyautogui.screenshot()
            screenShot.save(str(date_today) + "screenshot.png")

        #weather
        elif "what weather now" in command or "какая погода сейчас" in command:
             speek("Just a second, checking the weather.")
             weather = get_weather()

             if weather:
               speek(f"Температура {weather['temp']} градусов")
               speek(f"Ощущается как {weather['feels']} градусов")
               speek(f"На улице {weather['desc']}")

             else:
              speek("Не удалось получить данные о погоде")

        elif "jarvis" in command: 
             if len(command) < 10:
                speek("yes sir?")

    except Exception as e:
        print("Ошибка в цикле:", e)

    update_screen(screen, backg, font, weather)