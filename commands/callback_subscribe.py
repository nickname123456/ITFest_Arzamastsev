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
    
    # Если юзер до этого был не подписан:
    if db.get_any(user_id, data) == '0':
        # Теперь юзер подписан
        db.edit_any(user_id, data, '1')
        await bot.send_message(user_id, text=f'Ты успешно подписался на рассылку #{data}.')
    
    # Если юзер до этого был подписан
    else:
        # Теперь юзер не подписан
        db.edit_any(user_id, data, '0')
        await bot.send_message(user_id, text=f'Ты успешно отписался от рассылки #{data}.')
    