# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

# Создаем клавиатуру меню
menu_kb = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    .add(KeyboardButton('ℹИнформация'))
    .add(KeyboardButton('✔Подписки'), 
        KeyboardButton('🔓Доступные мероприятия'))
)

menu_inline_kb = (
    InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(InlineKeyboardButton('ℹИнформация', callback_data='information'))
    .add(InlineKeyboardButton('✔Подписки', callback_data='subscriptions'), 
        InlineKeyboardButton('🔓Доступные мероприятия', callback_data='available_events'))
)

adm_nenu_kb =(
    InlineKeyboardMarkup()
    .add(InlineKeyboardButton('Статистика', callback_data='adm_statistics'))
    .add(InlineKeyboardButton('Добавить', callback_data='add_event'),
        InlineKeyboardButton('Изменить', callback_data='edit'),
        InlineKeyboardButton('Удалить', callback_data='delete'))
)