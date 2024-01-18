from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import executor

from config import API_TOKEN
import handlers
from loguru import logger


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def main():
    handlers.register(dp)


if __name__ == '__main__':
    logger.info("Бот успешно запущен")
    main()
    executor.start_polling(dp, skip_updates=True)