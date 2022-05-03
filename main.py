# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from sqlighter import SQLighter

from settings import *
from private_data import TOKEN_TG, admin_password

from commands.admin.add_event import addEventState

from commands.start import start
from commands.menu import menu
from commands.help import help
from commands.callback_subscribe import callback_subscribe
from commands.callback_info import callback_info
from commands.callback import callback
from commands.notification import notification
from commands.admin.give_adm import give_adm
from commands.admin.add_event import add_event_start, add_event_name, add_event_link, add_event_hashtag, add_event_description
from commands.admin.cancel import cancel
from commands.admin.delete_event import delete_event_kb, callback_delete
from commands.admin.edit_event import edit_event_kb, edit_event_description,edit_event_hashtag,edit_event_link,edit_event_name, edit_event_start, editEventState


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot, storage=MemoryStorage())

db = SQLighter('it_fest.db')



# Команда старт
@dp.message_handler(commands=['start'], commands_prefix='/')
async def process_start_command(message: types.Message):
    await start(message)


# Команда меню
@dp.message_handler(commands=['menu', 'меню'], commands_prefix='/')
async def process_menu_command(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await menu(message)


# Команда помощь
@dp.message_handler(commands=['help', 'помощь'], commands_prefix='/')
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await help(message)


# Команда получения админки
@dp.message_handler(commands=admin_password, commands_prefix='/')
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await give_adm(message)



@dp.message_handler(commands=['delete', 'удалить'])
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await delete_event_kb(message)



@dp.message_handler(commands=['edit', 'изменить'])
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_kb(message)



@dp.message_handler(commands=['cancel', 'отмена'],state='*')
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await cancel(message, state)


# Команда добавления ивента
@dp.message_handler(commands=['add', 'addevent', 'добавить'])
async def process_add_event_start(message: types.Message):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_start(message)

@dp.message_handler(state=addEventState.name)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_name(message, state)

@dp.message_handler(state=addEventState.link)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_link(message, state)

@dp.message_handler(state=addEventState.hashtag)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_hashtag(message, state)

@dp.message_handler(state=addEventState.description)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_description(message, state)



@dp.message_handler(state=editEventState.name)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_name(message, state)

@dp.message_handler(state=editEventState.link)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_link(message, state)

@dp.message_handler(state=editEventState.hashtag)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_hashtag(message, state)

@dp.message_handler(state=editEventState.description)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_description(message, state)








# Обработка кэлбек кнопок с расылкой
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subscribe_'))
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_subscribe(callback_query)
    

# Обработка кэлбэк кнопок с информацией
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('info_'))
async def process_callback_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_info(callback_query)



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_'))
async def process_callback_delete(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_delete(callback_query)



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_'))
async def process_callback_delete(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_start(callback_query, state)


# Обработка всех остальных кэлбэк кнопок
@dp.message_handler(Text(equals=["ℹИнформация", '✔Подписки', '🔓Доступные мероприятия']))
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery=None):
    user_id = callback_query.from_user.id
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
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
    scheduler.add_job(notification, "interval", minutes=1)


# Если запустили этот файл, как главный:
if __name__ == '__main__':
    # Запускаем бота
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)