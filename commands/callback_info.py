# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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


async def callback_info(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = callback_query.data
    
    # Если данные из кэлбэк кнопки равно info_TechnoCom:
    if data == "info_TechnoCom":
        # Если человек подписан:
        if db.get_TechnoCom(callback_query.from_user.id) == '0':
            # Создаем клавиатуру
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_TechnoCom'))
            )
            # Отправляем сообщение
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #TechnoCom\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            # Создаем клавиатуру
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_TechnoCom'))
            )
            # Отправляем сообщение
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #TechnoCom\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_IT_fest_2022':
        if db.get_IT_fest_2022(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_IT_fest_2022'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #IT_fest_2022\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_IT_fest_2022'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #IT_fest_2022\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)


    elif data == 'info_IASF2022':
        if db.get_IASF2022(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_IASF2022'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #IASF2022\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_IASF2022'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #IASF2022\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_ФестивальОКК':
        if db.get_ФестивальОКК(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_ФестивальОКК'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #ФестивальОКК\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_ФестивальОКК'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #ФестивальОКК\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_Нейрофест':
        if db.get_Нейрофест(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_Нейрофест'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #Нейрофест\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_Нейрофест'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #Нейрофест\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_НевидимыйМир':
        if db.get_НевидимыйМир(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_НевидимыйМир'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #НевидимыйМир\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_НевидимыйМир'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #НевидимыйМир\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_КонкурсНИР':
        if db.get_КонкурсНИР(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_КонкурсНИР'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #КонкурсНИР\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_КонкурсНИР'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #КонкурсНИР\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)

    elif data == 'info_VRARFest3D':
        if db.get_VRARFest3D(callback_query.from_user.id) == '0':
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Подписаться', callback_data='subscribe_VRARFest3D'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #VRARFest3D\nСтатус: ❌Вы не подписаны❌', reply_markup=keyboard)
        else:
            keyboard = (
                InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                .add(InlineKeyboardButton('Отписаться', callback_data='subscribe_VRARFest3D'))
            )
            await bot.send_message(callback_query.from_user.id, text='Мероприятие: #VRARFest3D\nСтатус: ✅Вы подписаны✅', reply_markup=keyboard)
