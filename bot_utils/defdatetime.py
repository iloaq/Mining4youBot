import datetime
import pytz

now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
def date():
    return now.strftime("%d-%m-%Y")

def time():
    return now.strftime("%H:%M")