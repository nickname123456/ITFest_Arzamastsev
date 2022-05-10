# Импортируем библиотеки
import random
from PostgreSQLighter import SQLighter

from settings import *
import keyboard

# Подключаемся к бд
db = SQLighter('it_fest.db')

async def menu(message):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0: kb = keyboard.menu_kb
    else: kb = keyboard.menu_kb_for_adm

    # Отправляем сообщение с рандомным смайлом, и приветствием
    await message.reply(f"{random.choice(smiles)}{random.choice(greetings)} {message.from_user.first_name}, ты в главном меню!", reply_markup=kb)