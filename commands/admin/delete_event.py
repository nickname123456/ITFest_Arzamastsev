# Импортируем библиотеки
from aiogram import Bot, types
from sqlighter import SQLighter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import *
from private_data import TOKEN_TG

bot = Bot(token=TOKEN_TG)
db = SQLighter('it_fest.db') # Подключаемся к бд



async def delete_event_kb(message: types.Message):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return

    kb =InlineKeyboardMarkup(row_width=4)
    # Перебираем все ивенты
    events = db.get_all_from_events()
    for event in events:
        kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'delete_{event[0]}'))

    await message.answer('Какой ивент ты хочешь удалить?', reply_markup=kb)




async def callback_delete(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = str(callback_query.data)[7:]

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await bot.send_message(user_id, 'Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    db.delete_any_from_events(data) # Удаляем ивент
    await bot.send_message(user_id, f'Ты успешно удалил {data} !')