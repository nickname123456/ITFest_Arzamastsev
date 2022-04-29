# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter

from settings import *
from private_data import TOKEN_TG


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


async def start(message):
    try:
        # Если человека нет в бд, добавляем
        if db.get_id(message.from_user.id) is None:
            db.add_user(message.from_user.id)
    # Если вылезла ошибка, то тоже добавляем
    except TypeError:
        db.add_user(message.from_user.id)
    # Отправляем сообщение
    await message.reply("Привет!\nНапиши мне /menu, чтобы открыть главное меню!")
