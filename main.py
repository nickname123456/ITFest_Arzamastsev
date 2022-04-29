# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlighter import SQLighter

from settings import *
from private_data import TOKEN_TG

from commands.start import start
from commands.menu import menu
from commands.help import help
from commands.callback_subscribe import callback_subscribe
from commands.callback_info import callback_info
from commands.callback import callback
from commands.notification import notification


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')




# Команда старт
@dp.message_handler(commands=['start'], commands_prefix='/')
async def process_start_command(message: types.Message):
    await start(message)


# Команда меню
@dp.message_handler(commands=['menu', 'меню'], commands_prefix='/')
async def process_menu_command(message: types.Message):
    await menu(message)


# Команда помощь
@dp.message_handler(commands=['help', 'помощь'], commands_prefix='/')
async def process_help_command(message: types.Message):
    await help(message)



# Обработка кэлбек кнопок с расылкой
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subscribe_'))
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await callback_subscribe(callback_query)
    




# Обработка кэлбэк кнопок с информацией
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('info_'))
async def process_callback_info(callback_query: types.CallbackQuery):
    await callback_info(callback_query)




# Обработка всех остальных кэлбэк кнопок
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    await callback(callback_query)




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
    scheduler.add_job(notification, "interval", minutes=1, args=(dp,))


# Если запустили этот файл, как главный:
if __name__ == '__main__':
    # Запускаем бота
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)