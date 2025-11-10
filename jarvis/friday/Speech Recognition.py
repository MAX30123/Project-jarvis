import speech_recognition as sr

r = sr.Recognizer()


with sr.Microphone() as source:
    print("talk")
    audio_text = r.listen(source)
    try:
     text = r.recognize_sphinx()
     print("Text" + text)
    except:
       print("sorry o did not get that")