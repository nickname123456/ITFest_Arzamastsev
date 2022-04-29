# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter

from settings import *
import parser_vk
from private_data import TOKEN_TG


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


# Функция с рассылкой
async def notification(dp):
    # Перебираем ивенты
    for event in events:
        # Все юзеры, подписанные на этот ивент
        users = db.get_users_with_notification(event[1])
        # Получаем все посты этого ивента, а также новые, которые не числятся в бд
        all_posts, new_posts = await parser_vk.get_notification(event, db.get_old_posts(event[1]))
        # Записывваем в бд все посты
        db.edit_old_posts(event[1], all_posts)

        # Перебираем юзеров
        for user in users:
            # Перебираем новые посты
            for post in new_posts:
                # Отправляем пост юзеру
                await bot.send_message(user[0], post)
