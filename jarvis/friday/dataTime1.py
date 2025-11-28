import datetime

date = datetime.date(2026,4,12) # это что бы знать дату
print(date)

today = datetime.date.today() # это что бы знать сегодняшнюю дату
print(today)

time = datetime.time(12,5,30) # это что бы знать время
print(time)

now = datetime.datetime.now() # это что бы знать дату и время сейчас
print(now)

datetime_str = today.strftime(f"%Y,%m,%d")
print(datetime_str)