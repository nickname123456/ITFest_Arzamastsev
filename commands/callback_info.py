# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter

from settings import *
from private_data import TOKEN_TG


# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


async def callback_info(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    user_id = callback_query.from_user.id

    data = str(callback_query.data)
    name = data[5:]
    description = db.get_any_from_events('description', name)
    hashtag = db.get_any_from_events('hashtag', name)
    group_id = db.get_any_from_events('group_id', name)
    

    followers = eval(db.get_any_from_events('users', name))
    if user_id in followers:
        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Отписаться', callback_data=f'subscribe_{name}'))
        )
        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text=f'Название: {name}\nСсылка: {group_id}\nХэштег: {hashtag}\nОписание: {description}\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    else:
        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Подписаться', callback_data=f'subscribe_{name}'))
        )
        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text=f'Название: {name}\nСсылка: {group_id}\nХэштег: {hashtag}\nОписание: {description}\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)