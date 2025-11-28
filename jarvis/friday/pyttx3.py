import pyttsx3

engine = pyttsx3.init()
engine.say("hi im pyttxs3")
engine.runAndWait()

#это еще одна вариацыя для этого там можно контралеровать 

rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
engine.setProperty('volume', 1)
