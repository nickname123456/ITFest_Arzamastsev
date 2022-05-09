# Импортируем библиотеки
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from PostgreSQLighter import SQLighter

from keyboard import adm_nenu_kb
from settings import *
from private_data import TOKEN_TG


# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся к бд
db = SQLighter('it_fest.db')

async def adm_menu(message):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return

    await bot.send_message(user_id, 'Вот доступные инструменты для администраторов:', reply_markup=adm_nenu_kb)