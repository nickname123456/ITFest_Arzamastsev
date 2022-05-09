# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from PostgreSQLighter import SQLighter

from settings import *
from private_data import TOKEN_TG


# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся к бд
db = SQLighter('it_fest.db')


async def callback_info(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    user_id = callback_query.from_user.id

    # Получаем название ивента
    data = str(callback_query.data)
    name = data[5:] 
    # Получаем значения из бд
    try:
        description = db.get_any_from_events('description', name)
        hashtag = db.get_any_from_events('hashtag', name)
        group_id = db.get_any_from_events('group_id', name)
    
        followers = eval(db.get_any_from_events('users', name)) # Получаем всех юзеров, подписанных на этот ивент
    except TypeError:
        await callback_query.answer('❌Прости, но кажется этого ивента у меня нет в базе данных. Возможно его удалили') # Редактируем старое сообщение
        return

    if user_id in followers: # Если юзер подписан
        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Отписаться', callback_data=f'subscribe_{name}'))
        )
        status = '✅Вы подписаны✅'
    else: # Если не подписан
        keyboard = (
            InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            .add(InlineKeyboardButton('Подписаться', callback_data=f'subscribe_{name}'))
        )
        status = '❌Вы не подписаны❌'

    if db.get_any(user_id, 'is_admin') == 1: # Если юзер-админ, то добавляем админские кнопки)
        keyboard.add(InlineKeyboardButton('Изменить', callback_data=f'edit_{name}'))
        keyboard.insert(InlineKeyboardButton('Удалить', callback_data=f'delete_{name}'))

    # Отправляем сообщение
    await bot.send_message(callback_query.from_user.id, text=f'👀Название: {name}\n🙋‍♂️Число подписчиков: {len(followers)}\n🔗Ссылка: {group_id}\n#️⃣Хэштег: {hashtag}\n💢Описание: {description}\nСтатус: {status}', reply_markup=keyboard)