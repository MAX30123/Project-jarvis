import requests

API_KEY = "b3b1a603ceffddbe247b223101ec873d"
city = "Tel Aviv"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

response = requests.get(url)
data = response.json()


if data["cod"] == 200:
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]

    print(f"Температура: {temp}°C")
    print(f"Ощущается как: {feels}°C")
    print(f"Описание: {desc}")
else:
    print("Город не найден!")