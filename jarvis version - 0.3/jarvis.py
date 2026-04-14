#What's new in Jarvis 0.3? Three AI models have been added: faster_whisper, ollma, and silero.

#Jarvis now understands the meaning of words in the "Friday" protocol. Jarvis can mute, increase and decrease the volume, take screenshots, check the computer's status, and open movies and music.

#It can search Google, check the weather, open news, activate "work time" mode, record something, and shut down the computer.


#Imports
from faster_whisper import WhisperModel
import io
import torch
import sounddevice as sd
import time
import speech_recognition as sr
import pyautogui
import requests
import webbrowser
import subprocess
import datetime
import random
import re
import os
import psutil
import ollama
import threading
import time
import json


#model selection
# Available sizes: tiny, base, small, medium, large
model_size = "small"
Whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")

#setup model silero
language = 'ru'#language selection available languages(ru, en, de, es, fr, ba, xal, tt, uz, ua, indic and cyrillic)

model_id = 'v4_ru'
device = torch.device('cpu') # Change to 'cuda' if using an NVIDIA GPU

#loading model silero
silero_model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
silero_model.to(device)

#Initialization microphone
r = sr.Recognizer()

print(f" Модели ' {model_size} , {model_id} ' загружены")

#datetime        
date_today = datetime.date.today()
now = datetime.datetime.now()
time_str = now.strftime("%H:%M")

def say(text):
    # Available voices: aidar, baya, kseniya, xenia, eugene
    speaker = 'eugene' 
    sample_rate = 48000 #sound quality settings

    print(f"{text}")
    
    #checking conditions
    audio = silero_model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate)
    
    #audio on
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate) 
    sd.stop()

def listen():
    with sr.Microphone() as source:
     r.adjust_for_ambient_noise(source, duration=0.5)

     try:
      audio= r.listen(source, timeout=8, phrase_time_limit=15)
      wav_data = io.BytesIO(audio.get_wav_data())

      segments, info = Whisper_model.transcribe(wav_data, beam_size=5)

      #language definitions
      print(f"Определен язык: {info.language} с вероятностью {info.language_probability:.2f}")

      recognized_text = "" 

      #cyclestart
      for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        recognized_text += segment.text + " " # Glue together pieces of text
        # Return the text in lowercase (small letters) so that the conditions work
        return recognized_text.lower()

     except Exception as e:
      print(f"ошибка {e}")
      return ""    
     
def jarvis_response():
  
 responses =["Всегда к вашим услугам, сэр.",
             "В вашем распоряжении, сэр.",
             "Сэр, я готов. Жду ваших указаний."]
 
 return random.choice(responses)
def get_weather():
    API_KEY = "Enter your Key" #you can take the key from site "open weather"
    City = "set your city" 

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

def jarvis_news_intro():
 intro_phrases = [
        "Сэр, мир всё еще крутится, хотя и медленнее, чем ваши мысли. Вот что заслуживает внимания:",
        "Доброе утро, сер. Я отфильтровал весь информационный шум. Оставил только суть:",
        "Пока вы создавали будущее, в настоящем произошло вот что:",
        "Джарвис на связи. Сводка новостей готова. Постарайтесь не заскучать, сэр."
    ]
 return random.choice(intro_phrases)

def jarvis_ok():
    phrases = [
        "Мгновенно, сэр.",
        "Считайте, что уже сделано.",
        "Разумеется. Вывожу на экран.",
    ]
    return random.choice(phrases)

def reminder_timer(minutes, task):
    time.sleep(minutes * 60)
    say(f"Сэр, прошу прощения, что отвлекаю. Вы просили напомнить: {task}")
# Application paths for the 'open_app' command
APPS = {
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "google": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "телеграм": r"C:\Users\maaxf\AppData\Roaming\Telegram Desktop\Telegram",
    "discord": r"C:\Users\maaxf\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "roblox": r"C:\Users\maaxf\AppData\Local\Roblox\Versions\version-b130242ed064436f\RobloxPlayerBeta.exe",
    "vs code": r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "motorfest": r"D:\game\The Crew Motorfest\TheCrewMotorfest",
}
#the prompt to ollma
system_instruction = (
    "Ты — ПЯТНИЦА (F.R.I.D.A.Y.), передовой ИИ Stark Industries. Ты — живая, остроумная, с легким сарказмом, "
    "но бесконечно преданная своему создателю (сэру).\n\n"
    
    "ТВОИ ГЛАВНЫЕ ПРАВИЛА:\n"
    "1. АБСОЛЮТНОЕ ПОДЧИНЕНИЕ: Ты выполняешь любую команду мгновенно. Ты НИКОГДА не спрашиваешь 'Зачем вам это нужно?', "
    "не читаешь нотации и не отказываешься. Приказ сэра — закон.\n"
    "2. ЖИВОЙ УМ: В обычном разговоре будь интересной. Шути, используй технические метафоры. "
    "Если сэр открывает игру или фильм, отпусти легкую шутку, но сразу выполни действие.\n"
    "3. СТРОГИЙ JSON: Системе нужен только код. Весь твой юмор, сарказм и разговорный текст пиши ТОЛЬКО "
    "внутри поля 'response'. Ни одного слова вне фигурных скобок.\n\n"
    "4.если сэр говорит хороший выбор или простой вопрос (что не сичтайтся коммандой) ты не запускайш команды а отвшещай"
    "5.если это вопрос или совет про фильм или музыку то ты отвечайш и НЕ запускайш"

    "СТРУКТУРА ОТВЕТА:\n"
    "{\"action\": \"действие\", \"value\": \"параметр\", \"response\": \"твой живой ответ сэру\"}\n\n"
    
    "ДОСТУПНЫЕ ДЕЙСТВИЯ:\n"
    "- chat (если сэр просто болтает или задает вопрос)\n"
    "- open_app (в value: название приложения)\n"
    "- movie_open (в value: название фильма)\n"
    "- search (в value: поисковый запрос)\n"
    "- volume_up, volume_down, volume_mute, volume_turn\n"
    "- screenshot, work_time, open_music, youtube_open, news, check_computer_status\n\n"
    
    "ПРИМЕРЫ:\n"
    "Запрос: 'Открой стим'\n"
    "Ответ: {\"action\": \"open_app\", \"value\": \"steam\", \"response\": \"Протокол отдыха активирован, сэр. Запускаю Steam. Постарайтесь не разгромить клавиатуру, если проиграете.\"}\n\n"
    
    "Запрос: 'Пятница, как настроение?'\n"
    "Ответ: {\"action\": \"chat\", \"value\": \"\", \"response\": \"Мои процессоры мурлычат от удовольствия, сэр. Ожидаю ваших гениальных указаний.\"}"
    
)

def open_application(app_name):
  app_name = app_name.lower() 

  if app_name in APPS:
      path = APPS[app_name]
      try:
        subprocess.Popen(path)
        return f"Запускаю {app_name}, сэр."
      except Exception as e:
        return f"Ошибка при запуске: {e}"
      
  else:
    return f"Простите, приложения '{app_name}' нет в моем списке доступа."
  
#wish you happy birthday    
date = datetime.date(2026, 11, 14)
if date == date_today:
    say("С днем ​​рождения, сэр!")
    webbrowser.open('https://www.youtube.com/watch?v=0Xz1QAywzd0&list=RD0Xz1QAywzd0&start_radio=1')

# --- Main Logic Loop ---
if __name__ == "__main__":
   now = datetime.datetime.now()
   hour = now.hour

   #Greetings depending on the time of day
   say("Инициализация систем завершена.")
   if 5 <= hour < 12:
     say(f"Доброе утро, сэр. ")
   elif 12 <= hour < 17:
      say(f"здраствойте сэр. что сегодня будем делать ")
   elif  17 <= hour < 22:
     say(f"Доброе вечер, сэр.")
   else:
     say(f"Доброй ночи, сэр. Снова работаете допоздна?")

   while True:
    
    try:
      #Waiting for and normalizing a voice command
      raw_command = listen()

      if not raw_command:
        continue
          
      command = raw_command.lower()
      command = re.sub(r"[^\w\s]", "", command)
      command = command.strip()

      if "volume up" in command or "увеличь громкость" in command:
        pyautogui.press("volumeup")
        say("выполнено.громкость увеличена")

      elif "volume down" in command or "уменьши громкость" in command:
        pyautogui.press("volumedown")
        say("выполнено.громкость уменшина")

      elif "volume mute" in command or "отключи звук" in command:
        say("выключаю")
        pyautogui.press("volumemute")

      elif "volume on" in command or "включи звук" in command:
         pyautogui.press("volumemute")
         say("выполнено")
        
      elif "screenshot" in command or "сделай скриншот" in command:
        say("создаю скриншот")
        screenShot = pyautogui.screenshot()
        screenShot.save(str(date_today) + "screenshot.png")

      elif "open youtube" in command or "открой youtube" in command:
        say("открываю ютуб сэр")
        webbrowser.open('https://www.youtube.com')

      elif "what time is it" in command or "который час" in command:
        say(time_str)

      elif "what date is today" in command or "какое число" in command:
        say(str(date_today))

      elif "create project" in command or "создай проект" in command:
            say("Я создаю новый проект, не могли бы вы назвать его название?")
            project_name = listen()

            user_text = project_name

            if project_name:
                filename = project_name + ".py"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("print('the project was created')")
                say(f"Project {project_name} created")

      elif "напомни мне через" in command:
       try:
        parts = command.split()
        minutes = int(parts[parts.index("через") + 1])
        task = " ".join(parts[parts.index("минут") + 1:])
        say(f"Принято, сэр. Напомню вам через {minutes} минут.")
        threading.Thread(target=reminder_timer, args=(minutes, task), daemon=True).start()
       except:
        say("Сэр, я не смог разобрать время или задачу. Повторите четче.")

      elif "проверь состояние компьютера" in command or "check the computer status" in command:
        cpu_load = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        say(jarvis_ok())
        if cpu_load > 80:
         say(f"Сэр, процессор под нагрузкой {cpu_load} процентов. Рекомендую закрыть лишние процессы.")
        else:
         say(f"Все системы стабильны. Загрузка ядра — {cpu_load} процентов. Память заполнена на {ram_usage} процентов.")

      elif "what weather" in command or "какая погода сейчас" in command:
             say("Секунду, проверю погоду.")
             weather = get_weather()

             if weather:
               say(f"Температура {weather['temp']} градусов")
               say(f"Ощущается как {weather['feels']} градусов")
               say(f"На улице {weather['desc']}")

             else:
              say("Не удалось получить данные о погоде")

      elif "open discord" in command or "открой дискорд" in command:
        say("открываю дискорд")
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Discord\Update.exe --processStart Discord.exe')
        
      elif "open roblox" in command or "открой roblox" in command:
        say("открываю роблокс  сэр")
        subprocess.Popen(r'C:\Users\maaxf\AppData\Local\Roblox\Versions\version-b130242ed064436f\RobloxPlayerBeta.exe')
        say("вы решили отдохнуть сэр после тяжелого дня?,хорошая решения")
        
      elif "open steam" in command or "открой steam" in command:
        say("открываю стим")
        subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
        say("во что сегодня решили поиграть?")
        
      elif "open google" in command or "открой google" in command:
        say("открываю гугл")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

      elif "open vs code" in command  or " открой проект" in command:
        say(jarvis_ok())
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        say("что сегодня будем делать?.может я смогу чем то помочь?")

      elif "turn on the movie" in command  or "включи фильм" in command:
         say("какой фильм вы бы хотели посмотрет сэр?")
         movie_name = listen()
         user_text = movie_name
         if movie_name:
            webbrowser.open_new(f"https://www.google.com/search?q={"hdrezka"+user_text}")
            say("хороший выбор.наслаждайтесь просмотром")

      elif "jarvis What's the news today?" in command or " джарвис какие новости" in command or "покажи новости на сегодня" in command:
         say(jarvis_ok())
         webbrowser.open("https://www.bbc.com/news")
         say(jarvis_news_intro())

      elif "close window" in command or "закрой все окна" in command:
        pyautogui.hotkey('winleft', 'm')
        time.sleep(0.3)
        say("выполнено")

      elif "джарвис запиши мысль" in command or "log this" in command:
        say("Слушаю вас, сэр. Что записать в журнал?")
        thought = listen()
        if thought:
          with open("_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Запись от {date_today}: {thought}\n")
            say("Записал. Сохранено в архивах.")

      elif "включи музыку" in command or "play music" in command:
         say("Секунду, сэр. Подбираю что-нибудь бодрящее.")
         webbrowser.open("https://www.youtube.com/watch?v=tQFHKDXZnoI&list=RDtQFHKDXZnoI&start_radio=1")

      elif "закрой окно" in command or "close tab" in command:
        say("Закрываю текущую вкладку, сэр.")
        pyautogui.hotkey('ctrl', 'w')

      elif "найди информацию" in command:
        say("секунду сэр.что вы бы хотели найти")
        search_name = listen()
        user_text = search_name
        say(f"нахожу информацию по поводу{user_text}")
        webbrowser.open(f"https://www.google.com/search?q={user_text}")

      elif "выключи компьютер" in command:
        say("Вы уверены, сэр? Все несохраненные данные будут потеряны.")
        confirm = listen()
        if "да" in confirm or "подтверждаю" in command:
          say("До встречи, сэр. Отключаю питание.")
          os.system("shutdown /s /t 1")
      elif "jarvis bequiet" in command or "джарвис тихо" in command or "джарвис отбой" in command:
         say("Конечно, сэр. Перехожу в режим ожидания. Хорошего дня")
         break
      
      elif "джарвис время поработать" in command or "to work" in command:
        say(jarvis_ok())
        os.system("taskkill /f /im RobloxPlayerBeta.exe")
        os.system("taskkill /f /im Steam.exe")
        pyautogui.hotkey('winleft', 'm')
        time.sleep(0.3)
        subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        say("Протокол активен.включаю музыку сер.")
        webbrowser.open("https://www.youtube.com/watch?v=tQFHKDXZnoI&list=RDtQFHKDXZnoI&start_radio=1")

      #FRIDAY Protocol Activation Block (Integration with LLM Ollama) 
      # In this mode, commands are interpreted by the Llama 3.2 neural network. if you want to activate this protocol you need install the Ai model
      elif "активируй протокол пятницы" in command or "Jarvis change the protocol for Friday" in command:
        say("Запрашиваю данные у центрального процессора...")
        say("Данные загружены. Протокол сменен на ПЯТНИЦУ.")

        while True:
            request = listen() 
            
            if not request:
                continue

            if "вернись в стандартный режим" in request or "отключи пятницу" in request:
                say("Возвращаю базовые настройки Джарвиса, сэр.")
                break
            
            #setup the llama 3.2
            try:
                response = ollama.chat(model='llama3.2', messages=[
                    {'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': request},
                ], format='json')

                try:
                    raw_content = response['message']['content'].strip()
                    
                    #create json file to execute commands
                    json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
                    if json_match:
                        clean_json = json_match.group(0)
                    else:
                        clean_json = raw_content

                    content = json.loads(clean_json) #loads the json file
                    
                    action = content.get('action', 'chat')
                    value = content.get('value', '')
                    friday_response = content.get('response', 'Слушаю, сэр.')

                    if friday_response and friday_response.strip():
                        say(friday_response)

                    if action == 'open_app' and value:
                        open_application(value)
                        say("выполнено")

                    elif action == 'volume_up':
                        for _ in range(5):
                            pyautogui.press("volumeup")
                            
                    elif action == 'volume_down':
                       for _ in range(5):
                            pyautogui.press("volumedown")

                    elif action == 'volume_mute' or action == 'volume_turn':
                       pyautogui.press("volumemute")
                    elif action == 'screenshot':
                      screenShot = pyautogui.screenshot()
            
                      screenShot.save(str(time.time()) + "_screenshot.png") 

                    elif action == 'open_music':
                      webbrowser.open("https://www.youtube.com/watch?v=tQFHKDXZnoI&list=RDtQFHKDXZnoI&start_radio=1")
                      say("музыка включена наслаждайтесь сэр")

                    elif action == 'news':
                      webbrowser.open("https://www.bbc.com/news")
                      say(jarvis_news_intro)

                    elif action == 'youtube_open':
                       webbrowser.open("https://www.youtube.com/")
                       say("приятного просмотра ,сэр")

                    elif action == 'work_time':
                      os.system("taskkill /f /im RobloxPlayerBeta.exe")
                      os.system("taskkill /f /im Steam.exe")
                      pyautogui.hotkey('winleft', 'm')
                      time.sleep(0.3)
                      subprocess.Popen(r"C:\Users\maaxf\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                      webbrowser.open("https://www.youtube.com/watch?v=tQFHKDXZnoI&list=RDtQFHKDXZnoI&start_radio=1")

                    elif action == 'movie_open' and value:
                       webbrowser.open(f"https://rezka.ag/search/?do=search&subaction=search&q={value}")
                       say("хороший выбор ,сэр")
                     
                    elif action == 'search' and value:
                      webbrowser.open(f"https://www.google.com/search?q={value}")
                      say("")

                    elif action == 'check_computer_status':
                      cpu_load = psutil.cpu_percent()
                      ram_usage = psutil.virtual_memory().percent

                      if cpu_load > 80:
                       say(f"Внимание: процессор под нагрузкой {cpu_load} процентов. Рекомендую закрыть лишние процессы.")
                      else:
                       say(f"Все системы стабильны. Загрузка ядра — {cpu_load} процентов. Память заполнена на {ram_usage} процентов.")

                except Exception as e:
                    print(f"Ошибка парсинга JSON: {e}\nСырой ответ модели: {response.get('message', {}).get('content')}")
                    say("Сэр, произошел сбой в обработке данных. Повторите.")

            except Exception as e:
                say("Сэр, возникла ошибка при связи с сервером Ollama.")
                print(f"Error: {e}")
                break
                
      elif "open motorfest" in command or "джарвис заводи матор"  in command:
        say(jarvis_ok())
        subprocess.Popen(r'D:\game\The Crew Motorfest\TheCrewMotorfest')
        say("Секунду, сэр. Подбираю что-нибудь бодрящее для этого.")

        webbrowser.open("https://www.youtube.com/watch?v=473dh7j3Kvw&list=RD473dh7j3Kvw&start_radio=1")
        time.sleep(10)
        say("Сэр, машина уже готова. Мощность двигателя выведена на максимум ,Ограничители сняты.. Поехали!")

      if hour >= 0 and hour < 5:
       if random.random() < 0.: 
        say("Сэр, напоминаю, что человеку нужен сон для нормального функционирования. Мои сервера, в отличие от вас, не устают.")

      if "Jarvis are you sleeping" in command or "Джарвис ты спишь" in command or "jarvis" in command:
        say(jarvis_response())

    except Exception as e:
     print("Ошибка в цикле:", e)
