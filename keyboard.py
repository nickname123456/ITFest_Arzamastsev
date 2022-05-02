# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создаем клавиатуру меню
menu_kb = (
    InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(InlineKeyboardButton('ℹИнформация', callback_data='information'))
    .add(InlineKeyboardButton('✔Подписки', callback_data='subscriptions'), 
        InlineKeyboardButton('🔓Доступные мероприятия', callback_data='available_events'))
)