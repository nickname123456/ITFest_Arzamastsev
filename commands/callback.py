# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter
import random

from settings import *
import keyboard
from private_data import TOKEN_TG


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


async def callback(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = callback_query.data
    
    # Если дата = информация:
    if data == 'information':
        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text='Я - бот. Создан участником Международного Фестиваля Информационных Технологий! Служу для оповещания новых мероприятиях. Можете посмотреть все мои комманды в /help')
        await bot.send_message(callback_query.from_user.id, text='''
А если тебе интересно, то
Мой разработчик: Кирилл Арзамасцев
GitHub: https://github.com/nickname123456
Вк: https://vk.com/kirillarz
Дс: CoalNavl#0043
    ''')
    
    # Если дата = подписки:
    elif data == 'subscriptions':
        # Число проходов по дб
        n = 0
        # Номера ивентов, на которые подписан юзер
        event_numbers = []
        # Проверяем каждый ивент
        for i in db.get_all(callback_query.from_user.id):
            # Каждый круг добавляем к n 1
            n += 1
            # Если человек подписан на ивент:
            if i == '1':
                # Добавляем к номерам ивентов номер текущего ивента
                event_numbers.append(n)
        
        # Собираем текст по кусочкам
        text = f'{random.choice(text_subscriptions)}\n'
        for i in event_numbers:
            text += f'{events[i-2][1]}\n'

        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text=text)
    
    # Если дата = доступные ивенты
    elif data == 'available_events':
        # Отправляем сообщение с клавиатурой
        await bot.send_message(callback_query.from_user.id, text=random.choice(text_available_events), reply_markup=keyboard.subscriptions_kb)
