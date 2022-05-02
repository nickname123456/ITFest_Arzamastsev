# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter

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
    events = db.get_all_from_events()
    for event in events:
        # Все юзеры, подписанные на этот ивент
        users = eval(event[5])
        # Получаем все посты этого ивента, а также новые, которые не числятся в бд
        all_posts, new_posts = await parser_vk.get_notification(event[2], event[1], event[4])
        # Записывваем в бд все посты
        db.edit_any_from_events('old_posts', event[0], str(all_posts))

        # Перебираем юзеров
        for user in users:
            # Перебираем новые посты
            for post in new_posts:
                # Отправляем пост юзеру
                keyboard = (
                    InlineKeyboardMarkup()
                    .add(InlineKeyboardButton('Отписаться', callback_data=f'subscribe_{event[0]}'))
                )
                await bot.send_message(user, str(post), reply_markup=keyboard)
