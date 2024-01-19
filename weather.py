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


def request_forecast(city_id, day_number):
    try:
        russian_days = {'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда', 'Thursday': 'Четверг',
                        'Friday': 'Пятница', 'Saturday': 'Суббота', 'Sunday': 'Воскресенье'}

        russian_months = {'January': 'января', 'February': 'февраля', 'March': 'марта', 'April': 'апреля',
                          'May': 'мая', 'June': 'июня', 'July': 'июля', 'August': 'августа',
                          'September': 'сентября', 'October': 'октября', 'November': 'ноября', 'December': 'декабря'}

        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
        data = res.json()

        if 'list' not in data or not data['list']:
            return "‼️ Прогноз недоступен"

        if day_number < 1 or day_number > len(data['list']) // 8:
            return "‼️ Некоректний номер дня"

        start_index = (day_number - 1) * 8
        end_index = start_index + 24

        forecast_text = f"<b>⬇️ Прогноз погоды в {data['city']['name']}, {data['city']['country']} на {day_number}-й день ⬇️</b>\n"
        current_day = None

        for i in range(start_index, end_index, 2):
            if i >= len(data['list']):
                break

            current_data = data['list'][i]

            if 'dt_txt' not in current_data or 'main' not in current_data or 'weather' not in current_data or 'wind' not in current_data:
                continue

            dt_obj = datetime.datetime.strptime(current_data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            day_of_week = dt_obj.strftime('%A')
            month_name = dt_obj.strftime('%B')

            russian_day = russian_days.get(day_of_week, day_of_week)
            russian_month = russian_months.get(month_name, month_name)

            formatted_date = dt_obj.strftime(f'%d {russian_month} %Y')  # Format the date as "day month year"

            day = dt_obj.strftime('%Y-%m-%d')
            specified_day = (datetime.datetime.now() + datetime.timedelta(days=day_number)).strftime('%Y-%m-%d')

            if day != specified_day:
                continue

            if day != current_day:
                forecast_text += f"\n📆 <b>{russian_day}, {formatted_date}</b>\n"
                current_day = day

            forecast_text += f"\n<b>{dt_obj.strftime('%H:%M')}</b>\n<i>{current_data['weather'][0]['description']},\n" \
                             f"<b>🌡 Температура:</b> {current_data['main']['temp']}°C, \n" \
                             f"<b>💨 Скорость ветра:</b> {current_data['wind']['speed']} м/с, \n" \
                             f"<b>↔️ Направление ветру:</b> {get_wind_direction(current_data['wind']['deg'])}\n</i>"

        return forecast_text
    except Exception as e:
        logger.error("Exception (forecast):", e)
        return "‼️ Произошла ошибка при получении прогноза."
