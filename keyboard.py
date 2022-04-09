# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создаем клавиатуру меню
menu_kb = (
    InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(InlineKeyboardButton('ℹИнформация', callback_data='information'))
    .add(InlineKeyboardButton('✔Подписки', callback_data='subscriptions'), 
        InlineKeyboardButton('🔓Доступные мероприятия', callback_data='available_events'))
)

# Создаем клавиатуру подписок
subscriptions_kb =(InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(InlineKeyboardButton('#TechnoCom', callback_data='info_TechnoCom'), 
        InlineKeyboardButton('#IT_fest_2022 ', callback_data='info_IT_fest_2022'),
        InlineKeyboardButton('#IASF2022 ', callback_data='info_IASF2022'),
        InlineKeyboardButton('#ФестивальОКК ', callback_data='info_ФестивальОКК'),
        InlineKeyboardButton('#Нейрофест ', callback_data='info_Нейрофест'),
        InlineKeyboardButton('#НевидимыйМир ', callback_data='info_НевидимыйМир'),
        InlineKeyboardButton('#КонкурсНИР ', callback_data='info_КонкурсНИР'),
        InlineKeyboardButton('#VRARFest3D', callback_data='info_VRARFest3D'))
)