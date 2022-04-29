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


async def help(message):
    # Отправляем сообщение
    await message.reply("Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:\nГруппа ВКонтакте Научим.online https://vk.com/nauchim.online\nСайт с мероприятиями https://www.научим.online")
    await message.reply("Вот все мои команды:\n/start - регистрирует вас в базе данных, если вы в ней не зачислены\n/menu - Отправляет главное меню")