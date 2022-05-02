# Импортируем библиотеки
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import *
from private_data import TOKEN_TG


# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')


async def callback(query: types.CallbackQuery):
    if isinstance(query, types.CallbackQuery):
        # Что хранится в колбек кнопке
        data = query.data
        user_id = query.from_user.id
        
        # Если дата = информация:
        if data == 'information':
            # Отправляем сообщение
            await bot.send_message(query.from_user.id, text='Я - бот. Создан участником Международного Фестиваля Информационных Технологий! Служу для оповещания новых мероприятиях. Можете посмотреть все мои комманды в /help')
            await bot.send_message(query.from_user.id, text='''
    А если тебе интересно, то
    Мой разработчик: Кирилл Арзамасцев
    GitHub: https://github.com/nickname123456
    Вк: https://vk.com/kirillarz
    Дс: CoalNavl#0043
        ''')
        
        # Если дата = подписки:
        elif data == 'subscriptions':
            subscriptions_kb =InlineKeyboardMarkup(row_width=4)

            events = db.get_all_from_events()
            for event in events:
                if user_id in eval(event[5]):
                    subscriptions_kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'info_{event[0]}'))

            if len(subscriptions_kb.inline_keyboard) > 0:
                await bot.send_message(query.from_user.id, text=random.choice(text_subscriptions), reply_markup=subscriptions_kb)
            else:
                subscriptions_kb.insert(InlineKeyboardButton('🔓Доступные мероприятия', callback_data='available_events'))
                await bot.send_message(query.from_user.id, text='Ты ни на что не подписан.', reply_markup=subscriptions_kb)
        
        # Если дата = доступные ивенты
        elif data == 'available_events':
            subscriptions_kb =InlineKeyboardMarkup(row_width=4)

            events = db.get_all_from_events()
            for event in events:
                subscriptions_kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'info_{event[0]}'))

            await bot.send_message(query.from_user.id, text=random.choice(text_available_events), reply_markup=subscriptions_kb)




    elif isinstance(query, types.Message):
        user_id = query.from_user.id
        text = query.text
        
        # Если дата = информация:
        if text == 'ℹИнформация':
            # Отправляем сообщение
            await bot.send_message(query.from_user.id, text='Я - бот. Создан участником Международного Фестиваля Информационных Технологий! Служу для оповещания новых мероприятиях. Можете посмотреть все мои комманды в /help')
            await bot.send_message(query.from_user.id, text='''
    А если тебе интересно, то
    Мой разработчик: Кирилл Арзамасцев
    GitHub: https://github.com/nickname123456
    Вк: https://vk.com/kirillarz
    Дс: CoalNavl#0043
        ''')
        
        # Если дата = подписки:
        elif text == '✔Подписки':
            subscriptions_kb =InlineKeyboardMarkup(row_width=4)

            events = db.get_all_from_events()
            for event in events:
                if user_id in eval(event[5]):
                    subscriptions_kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'info_{event[0]}'))

            if len(subscriptions_kb.inline_keyboard) > 0:
                await bot.send_message(query.from_user.id, text=random.choice(text_subscriptions), reply_markup=subscriptions_kb)
            else:
                subscriptions_kb.insert(InlineKeyboardButton('🔓Доступные мероприятия', callback_data='available_events'))
                await bot.send_message(query.from_user.id, text='Ты ни на что не подписан.', reply_markup=subscriptions_kb)
        
        # Если дата = доступные ивенты
        elif text == '🔓Доступные мероприятия':
            subscriptions_kb =InlineKeyboardMarkup(row_width=4)

            events = db.get_all_from_events()
            for event in events:
                subscriptions_kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'info_{event[0]}'))

            await bot.send_message(query.from_user.id, text=random.choice(text_available_events), reply_markup=subscriptions_kb)
