from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Больше информации", callback_data='main')]]
    )
    return markup


def main_keyboard_data() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("1", callback_data='main_1'),
         InlineKeyboardButton("2", callback_data='main_2'),
         InlineKeyboardButton("3", callback_data='main_3'),
         InlineKeyboardButton("4", callback_data='main_4')],
         [InlineKeyboardButton("Удалить", callback_data='main_delete')]]
    )
    return markup
