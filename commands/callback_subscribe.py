# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
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


async def callback_subscribe(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = str(callback_query.data)[10:]
    # id юзера
    user_id = callback_query.from_user.id
    
    followers = eval(db.get_any_from_events('users', data))

    if user_id in followers:
        followers.remove(user_id)
        text = f'Ты успешно отписался от рассылки {data}.'
    else:
        followers.append(user_id)
        text = f'Ты успешно подписался на рассылку {data}.'
    
    db.edit_any_from_events('users', data, str(followers))
    
    await bot.send_message(user_id, text=text)