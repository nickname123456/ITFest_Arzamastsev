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


async def adm_statistics(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await callback_query.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return

    num_of_users = len(db.get_all())
    num_of_events = len(db.get_all_from_events())
    admins = [user for user in db.get_all() if user[1] == 1]
    num_of_admins = len(admins)
    admins_id = [admin[0] for admin in admins]

    text = f"Текущая статистика: \n👽Число пользователей: {num_of_users}\n🎊Число ивентов: {num_of_events}\n🤡Число администраторов: {num_of_admins}\n🆔'шники администраторов: {str(admins_id)}"

    await bot.send_message(user_id, text)