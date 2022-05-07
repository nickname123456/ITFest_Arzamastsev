# Импортируем библиотеки
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import *
from private_data import TOKEN_TG


# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся к бд
db = SQLighter('it_fest.db')


async def callback_subscribe(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = str(callback_query.data)[10:]
    # id юзера
    user_id = callback_query.from_user.id
    
    followers = eval(db.get_any_from_events('users', data)) # Подписчики ивента

    if user_id in followers: # Если юзер подписан
        followers.remove(user_id) # Отписываемся
        await callback_query.answer(f'Ты успешно отписался от рассылки {data}.')

        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Подписаться', callback_data=f'subscribe_{data}'))
        )
        status = '❌Вы не подписаны❌'
    else:
        followers.append(user_id) # Подписываемся
        await callback_query.answer(f'Ты успешно подписался на рассылку {data}.')

        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Отписаться', callback_data=f'subscribe_{data}'))
        )
        status = '✅Вы подписаны✅'
    
    if db.get_any(user_id, 'is_admin') == 1: # Если юзер-админ, то добавляем админ кнопки
        keyboard.add(InlineKeyboardButton('Изменить', callback_data=f'edit_{data}'))
        keyboard.insert(InlineKeyboardButton('Удалить', callback_data=f'delete_{data}'))

    db.edit_any_from_events('users', data, str(followers)) # Вносим изменения в бд
    # Получаем информацию из бд
    name = data
    description = db.get_any_from_events('description', name)
    hashtag = db.get_any_from_events('hashtag', name)
    group_id = db.get_any_from_events('group_id', name)
    # По кусочкам собираем текст
    text = f'Название: {name}\nСсылка: {group_id}\nХэштег: {hashtag}\nОписание: {description}\nСтатус: {status}'
    
    await bot.edit_message_text(text, user_id, callback_query.message.message_id) # Редактируем старое сообщение
    await bot.edit_message_reply_markup(user_id, callback_query.message.message_id, reply_markup=keyboard) # Говорим пользователю, что отписали/подписали его