import webbrowser

x = input("выдите слово youtube ,twich или gmail: ")

if x == "youtube":
    webbrowser.open_new('https://www.youtube.com/') # open_new откройт в новом окне
elif x == "twich":
    webbrowser.open('https://www.twitch.tv/') #open просто откройт
elif x == "gmail":
    webbrowser.open_new_tab('https://mail.google.com/mail/u/0/#inbox') #откройт в новай страничке 