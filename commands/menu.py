# Импортируем библиотеки
import random

from settings import *
import keyboard

async def menu(message):
    # Отправляем сообщение с рандомным смайлом, и приветствием
    await message.reply(f"{random.choice(smiles)}{random.choice(greetings)} {message.from_user.first_name}, ты в главном меню!", reply_markup=keyboard.menu_kb)