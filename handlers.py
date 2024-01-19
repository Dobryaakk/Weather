import datetime
from loguru import logger
from aiogram import types, Dispatcher
from weather import get_city_id, request_current_weather, request_forecast

from run_bot import bot
from keyboard import main_keyboard, main_keyboard_data

city_id = None


async def on_start(message: types.Message):
    await message.answer("<b>Привет!</b> Это бот для получения погоды ⛅️\nВведите <code>/weather 'Ваш город'</code> для получения прогноза погоды.\n\n"
                         "<i>Автор @dobrychek</i>", parse_mode='HTML')


async def on_weather(message: types.Message):
    global city_id
    try:
        args = message.get_args().split(' ')
        if len(args) >= 1:
            city_name = args[0]
            city_id = get_city_id(city_name)

            if city_id is not None:
                weather_data, feather_coo, city_timezone = request_current_weather(city_id)

                local_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=city_timezone)
                logger.info(local_time)
                logger.info(feather_coo)

                if 6 <= local_time.hour < 18:
                    if feather_coo == 'небольшой дождь' or feather_coo == 'дождь':
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_4_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(),
                                             parse_mode='HTML')
                    elif feather_coo == 'пасмурно' or feather_coo == 'хмарно' or feather_coo == 'туман' or feather_coo == 'небольшая облачность' or feather_coo == 'плотный туман':
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_2_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'небольшой снег' or feather_coo == 'снег':
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_6_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'ясно':
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_9_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'гроза':
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_7_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    else:
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_2_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')

                else:
                    if feather_coo == 'небольшой дождь' or feather_coo == 'дождь':
                        await bot.send_photo(message.chat.id,
                                             photo=open('weather_night/photo_3_2024-01-18_19-11-37.jpg',
                                                        'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'пасмурно' or feather_coo == 'хмарно' or feather_coo == 'туман' or feather_coo == 'небольшая облачность' or feather_coo == 'плотный туман':
                        await bot.send_photo(message.chat.id,
                                             photo=open('weather_night/photo_8_2024-01-18_19-11-37.jpg',
                                                        'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'небольшой снег' or feather_coo == 'снег':
                        await bot.send_photo(message.chat.id,
                                             photo=open('weather_night/photo_5_2024-01-18_19-11-37.jpg',
                                                        'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'ясно':
                        await bot.send_photo(message.chat.id,
                                             photo=open('weather_night/photo_10_2024-01-18_19-11-37.jpg',
                                                        'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    elif feather_coo == 'гроза':
                        await bot.send_photo(message.chat.id,
                                             photo=open('weather_night/photo_1_2024-01-18_19-11-37.jpg',
                                                        'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
                    else:
                        await bot.send_photo(message.chat.id, photo=open('weather_day/photo_2_2024-01-18_19-11-37.jpg',
                                                                         'rb'), caption=weather_data,
                                             reply_markup=main_keyboard(), parse_mode='HTML')
            else:
                await message.answer("‼️ Не удалось распознать город")

    except ValueError as ex:
        logger.error(ex)


async def main_key(callback: types.CallbackQuery):
    if callback.data == 'main':
        await callback.message.answer("Выберите на сколько дней вперед вы хотите увидеть прогноз погоды 🌤", reply_markup=main_keyboard_data(), parse_mode='HTML')
    elif callback.data in ['main_1', 'main_2', 'main_3', 'main_4']:
        days = int(callback.data[-1])
        await callback.message.edit_text(request_forecast(city_id, days), reply_markup=main_keyboard_data(), parse_mode='HTML')
    if callback.data == 'main_delete':
        await callback.message.delete()


def register(dp: Dispatcher):
    dp.register_message_handler(on_start, commands=['start', 'help'])
    dp.register_message_handler(on_weather, commands=['weather'])
    dp.register_callback_query_handler(main_key, lambda callback_query: callback_query.data.startswith('main'))
