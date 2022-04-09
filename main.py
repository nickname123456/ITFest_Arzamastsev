# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlighter import SQLighter
import random

from settings import *
import keyboard
import parser_vk


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')




# Команда старт
@dp.message_handler(commands=['start'], commands_prefix='/')
async def process_start_command(message: types.Message):
    try:
        # Если человека нет в бд, добавляем
        if db.get_id(message.from_user.id) is None:
            db.add_user(message.from_user.id)
    # Если вылезла ошибка, то тоже добавляем
    except TypeError:
        db.add_user(message.from_user.id)
    # Отправляем сообщение
    await message.reply("Привет!\nНапиши мне /menu, чтобы открыть главное меню!")


# Команда меню
@dp.message_handler(commands=['menu', 'меню'], commands_prefix='/')
async def process_start_command(message: types.Message):
    # Отправляем сообщение с рандомным смайлом, и приветствием
    await message.reply(f"{random.choice(smiles)}{random.choice(greetings)} {message.from_user.first_name}, ты в главном меню!", reply_markup=keyboard.menu_kb)

# Команда помощь
@dp.message_handler(commands=['help', 'помощь'], commands_prefix='/')
async def process_start_command(message: types.Message):
    # Отправляем сообщение
    await message.reply("Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:\nГруппа ВКонтакте Научим.online https://vk.com/nauchim.online\nСайт с мероприятиями https://www.научим.online")
    await message.reply("Вот все мои команды:\n/start - регистрирует вас в базе данных, если вы в ней не зачислены\n/menu - Отправляет главное меню")




# Обработка кэлбек кнопок с расылкой
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subscribe_'))
async def process_callback_info(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = str(callback_query.data)[10:]
    # id юзера
    user_id = callback_query.from_user.id
    
    # Если юзер до этого был не подписан:
    if db.get_any(user_id, data) == '0':
        # Теперь юзер подписан
        db.edit_any(user_id, data, '1')
        await bot.send_message(user_id, text=f'Ты успешно подписался на рассылку #{data}.')
    
    # Если юзер до этого был подписан
    else:
        # Теперь юзер не подписан
        db.edit_any(user_id, data, '0')
        await bot.send_message(user_id, text=f'Ты успешно отписался от рассылки #{data}.')
    




# Обработка кэлбэк кнопок с информацией
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('info_'))
async def process_callback_info(callback_query: types.CallbackQuery):
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



# Обработка всех остальных кэлбэк кнопок
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    # Что хранится в колбек кнопке
    data = callback_query.data
    
    # Если дата = информация:
    if data == 'information':
        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text='Я - бот. Создан участником Международного Фестиваля Информационных Технологий! Служу для оповещания новых мероприятиях. Можете посмотреть все мои комманды в /help')
    
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
        text = 'На данный момент ты подписан на:\n'
        for i in event_numbers:
            text += f'{events[i-2][1]}\n'

        # Отправляем сообщение
        await bot.send_message(callback_query.from_user.id, text=text)
    
    # Если дата = доступные ивенты
    elif data == 'available_events':
        # Отправляем сообщение с клавиатурой
        await bot.send_message(callback_query.from_user.id, text='Вот список мероприятий, на которые ты можешь подписаться:', reply_markup=keyboard.subscriptions_kb)





# Функция с рассылкой
async def notiication(dp):
    # Перебираем ивенты
    for event in events:
        # Все юзеры, подписанные на этот ивент
        users = db.get_users_with_notification(event[1])
        # Получаем все посты этого ивента, а также новые, которые не числятся в бд
        all_posts, new_posts = await parser_vk.get_notification(event, db.get_old_posts(event[1]))
        # Записывваем в бд все посты
        db.edit_old_posts(event[1], all_posts)

        # Перебираем юзеров
        for user in users:
            # Перебираем новые посты
            for post in new_posts:
                # Отправляем пост юзеру
                await bot.send_message(user[0], post)


# Запускается при старте программы
async def on_startup(dp):
    # Информация про меня)
    print('')
    print('-------------------------------')
    print('  Скрипт бота тг для итфеста запущен.')
    print('  Разработчик: Кирилл Арзамасцев ')
    print('  GitHub: https://github.com/nickname123456')
    print('  Вк: https://vk.com/kirillarz')
    print('  Дс: CoalNavl#0043')
    print('-------------------------------')
    print('')

    # Каждые 60 минут запускаем рассылку
    scheduler.add_job(notiication, "interval", minutes=60, args=(dp,))


# Если запустили этот файл, как главный:
if __name__ == '__main__':
    # Запускаем бота
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)