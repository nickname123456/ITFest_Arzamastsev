# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter
import random

from settings import *
from private_data import TOKEN_TG
import keyboard


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


async def give_adm(message):
    # Отправляем сообщение с рандомным смайлом, и приветствием
    await message.reply('Адм хошь?')