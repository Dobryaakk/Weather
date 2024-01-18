import requests
from config import APPID
import datetime
from loguru import logger

def get_wind_direction(deg):
    l = ['Северное ','Северное-восточное',' Восточное','Юго-восточное','Южное ','Юго-западное',' Западное','Северо-западное']
    for i in range(0, 8):
        step = 45.
        min = i * step - 45/2.
        max = i * step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360

        if deg >= min and deg <= max:
            return l[i]


def get_city_id(s_city_name, country_code=''):
    try:
        params = {'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': APPID}
        if country_code:
            params['country'] = country_code
        res = requests.get("http://api.openweathermap.org/data/2.5/find", params=params)
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
        print("city:", cities)
        if data['list']:
            city_id = data['list'][0]['id']
            print('city_id=', city_id)
            return city_id
        else:
            return None
    except Exception as e:
        print("Exception (find):", e)
        return None


def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
        data = res.json()
        conditions = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        wind_speed = data['wind']['speed']
        wind_direction = get_wind_direction(data['wind']['deg'])
        timezone = data['timezone']

        k = f"<b>⬇️ Погода в {data['name']}, {data['sys']['country']}: ⬇️\n\n</b>" \
               f"🔸 Сейчас: {conditions}\n" \
               f"🌡 Температура: {temp}°C\n" \
               f"📉 Мин. температура: {temp_min}°C\n" \
               f"📈 Макс. температура: {temp_max}°C\n" \
               f"💨 Скорость ветра: {wind_speed} м/с\n" \
               f"↔️ Направление ветра: {wind_direction}"

        return k, conditions, timezone

    except Exception as e:
        logger.error("Exception (weather):", e)
        return "‼️ Произошла ошибка при получении погоды."


def request_forecast(city_id, days):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
        data = res.json()

        if 'list' not in data or not data['list']:
            return "‼️ Прогноз недоступен"

        forecast_text = f"<b>⬇️ Прогноз погоды в {data['city']['name']}, {data['city']['country']} на {days}д. ⬇️</b>\n"
        current_day = None

        for i in data['list'][:days * 8]:
            if 'dt_txt' not in i or 'main' not in i or 'weather' not in i or 'wind' not in i:
                continue

            day = datetime.datetime.strptime(i['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

            if day != current_day:
                forecast_text += '\n\n'
                current_day = day

            forecast_text += f"<b>{i['dt_txt'][:16]}</b>\n<i>{i['weather'][0]['description']},\n" \
                             f"<b>🌡 Температура:</b> {i['main']['temp']}°C, \n" \
                             f"<b>💨 Скорость ветра:</b> {i['wind']['speed']} м/с, \n" \
                             f"<b>↔️ Направление ветру:</b> {get_wind_direction(i['wind']['deg'])}\n</i>\n"

        return forecast_text
    except Exception as e:
        logger.error("Exception (forecast):", e)
        return "‼️ Произошла ошибка при получении прогноза."