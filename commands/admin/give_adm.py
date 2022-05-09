# Импортируем библиотеки
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from PostgreSQLighter import SQLighter

from settings import *
from private_data import TOKEN_TG

# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся к бд
db = SQLighter('it_fest.db')


async def give_adm(message):
    # id юзера
    user_id = message.from_user.id

    db.edit_any(user_id, 'is_admin', 1) # Выдаем админку
    await bot.send_message(user_id, text='😏Тебе была выдана возможность администрирования! Посмотреть админ-команды можно посмотреть в /help')