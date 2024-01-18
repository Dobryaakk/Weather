from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Больше информации", callback_data='main_1')]]
    )
    return markup


def main_keyboard_data() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("1", callback_data='main_2'),
         InlineKeyboardButton("2", callback_data='main_3'),
         InlineKeyboardButton("3", callback_data='main_4'),
         InlineKeyboardButton("4", callback_data='main_5')]]
    )
    return markup
