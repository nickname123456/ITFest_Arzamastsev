# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from PostgreSQLighter import SQLighter

from settings import *
from private_data import TOKEN_TG, admin_password

from commands.admin.add_event import addEventState
from commands.admin.edit_event import editEventState

# Импортируем все команды
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
from commands.admin.edit_event import edit_event_kb, edit_event_description,edit_event_hashtag,edit_event_link,edit_event_name, edit_event_start
from commands.admin.adm_panel import adm_menu, adm_statistics


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключение к бд
db = SQLighter('it_fest.db')

# ```````````````````БАЗА```````````````````````````````````````

# Команда старт
@dp.message_handler(commands=['start'], commands_prefix='/')
async def process_start_command(message: types.Message):
    await start(message)


# Команда меню
@dp.message_handler(commands=['menu', 'меню'], commands_prefix='/')
async def process_menu_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await menu(message)


# Команда админ меню
@dp.callback_query_handler(lambda c: c.data and c.data =='admin_menu')
@dp.message_handler(commands=['admmenu', 'адмменю', 'admpanel'], commands_prefix='/')
async def process_menu_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await adm_menu(message)


# Команда помощь
@dp.message_handler(commands=['help', 'помощь'], commands_prefix='/')
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await help(message)


# `````````````````````````````````````````````````АДМИН КОМАНДЫ````````````````````````````````````````````````````````````````````````````````

# Команда получения админки
@dp.message_handler(commands=admin_password, commands_prefix='/')
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await give_adm(message)


@dp.message_handler(commands=['adm_statistics', 'admstatistics', 'стата', 'статистика', 'stata'])
@dp.callback_query_handler(lambda c: c.data and c.data =='adm_statistics')
async def statistics(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await adm_statistics(message)

# Команда удаления ивента
@dp.callback_query_handler(lambda c: c.data and c.data =='delete')
@dp.message_handler(commands=['delete', 'удалить'])
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await delete_event_kb(message)


# Команда изменения ивента
@dp.callback_query_handler(lambda c: c.data and c.data =='edit')
@dp.message_handler(commands=['edit', 'изменить'])
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_kb(message)


# Команда отмены
@dp.message_handler(commands=['cancel', 'отмена'],state='*')
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await cancel(message, state)


# ````````````````````СТЕЙТЫ ДОБАВЛЕНИЯ ИВЕНТОВ```````````````````````````````````````

# Команда добавления ивента
@dp.callback_query_handler(lambda c: c.data and c.data =='add_event')
@dp.message_handler(commands=['add', 'addevent', 'добавить'])
async def process_add_event_start(message: types.Message):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_start(message)

# Получение названия нового ивента
@dp.message_handler(state=addEventState.name)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_name(message, state)

# Получение ссылки нового ивента
@dp.message_handler(state=addEventState.link)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_link(message, state)

# Получение хэштега нового ивента
@dp.message_handler(state=addEventState.hashtag)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_hashtag(message, state)

# Получение описания нового ивента
@dp.message_handler(state=addEventState.description)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await add_event_description(message, state)


# ````````````````````СТЕЙТЫ ИЗМЕНЕНИЯ ИВЕНТОВ```````````````````````````````````````


# Получение названия изменяемого ивента
@dp.message_handler(state=editEventState.name)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_name(message, state)

# Получение ссылки изменяемого ивента
@dp.message_handler(state=editEventState.link)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_link(message, state)

# Получение хэштега изменяемого ивента
@dp.message_handler(state=editEventState.hashtag)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_hashtag(message, state)

# Получение описания изменяемого ивента
@dp.message_handler(state=editEventState.description)
async def process_help_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await message.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_description(message, state)





# ````````````````````КОЛЛБЭКИ```````````````````````````````````````


# Обработка кнопки, когда у ивента нет хэштега
@dp.callback_query_handler(lambda c: c.data and c.data == 'add_non_hashtag', state=addEventState.hashtag)
async def process_callback_add_non_hashtag(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await callback_query.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await state.update_data(hashtag='')
    await addEventState.next()
    await bot.send_message(user_id, "😲Нет хэштега? Ну ничего страшного! Я буду рассылать все посты из указанного паблика. А теперь введи краткое описание ивента")


# Обработка кнопки, когда у ивента остается что-то старое
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_keep_'), state='*')
async def process_callback_add_non_hashtag(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await callback_query.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    
    # объект равен ...
    obj = callback_query.data[10:]
    if obj == 'name':
        await state.update_data(name='keep_old') # Задаем значение в хранилище
        await editEventState.next() # Переходим на следующий этап
        await bot.send_message(user_id, "👍Хорошо, оставляю старое название. Теперь введи ссылку на сообщество вк", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Оставить прежнию ссылку', callback_data=f'edit_keep_link')))
    elif obj == 'link':
        await state.update_data(link='keep_old')
        await editEventState.next()
        await bot.send_message(user_id, '👍Хорошо, оставляю старую ссылку. Теперь введи хэштег, если он есть. Если нет, то напиши "нет"', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Оставить прежний хэштег', callback_data=f'edit_keep_hashtag')))
    elif obj == 'hashtag':
        await state.update_data(hashtag='keep_old')
        await editEventState.next()
        await bot.send_message(user_id, '👍Хорошо, оставляю старый хэштег. Теперь введи краткое описание ивента', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Оставить прежнее описание', callback_data=f'edit_keep_description')))
    
    elif obj == 'description':
        await state.update_data(description='keep_old')
        user_data = await state.get_data()
        old_name = user_data['old_name'] # Старое название

        if user_data['link'] == 'keep_old': group_id = db.get_any_from_events('group_id',old_name) # Если надо оставить старую ссылку
        else: group_id = user_data['link'] # Если не надо оставить старую ссылку

        if user_data['name'] == 'keep_old': name = db.get_any_from_events('name',old_name)
        else: name = user_data['name']
        
        if user_data['hashtag'] == 'keep_old': hashtag = db.get_any_from_events('hashtag',old_name)
        else: hashtag = user_data['hashtag']
        
        if user_data['description'] == 'keep_old': description = db.get_any_from_events('description',old_name)
        else: description = user_data['description']

        # Изменяем ивент
        db.edit_any_from_events('group_id', old_name, group_id)
        db.edit_any_from_events('hashtag', old_name, hashtag)
        db.edit_any_from_events('description', old_name, description)
        db.edit_any_from_events('name', old_name, name)

        # Создаем клавиатуру
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}'))

        await bot.send_message(user_id, "✅Твой ивент успешно обновлен! Хочешь посмотреть?", reply_markup=keyboard)
        await state.finish() # Заканчиваем


    
    


# Обработка кэлбек кнопок с подпиской
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subscribe_'))
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_subscribe(callback_query)
    

# Обработка кэлбэк кнопок с информацией
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('info_'))
async def process_callback_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_info(callback_query)


# Обработка кнопки удаления ивента
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_'))
async def process_callback_delete(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback_delete(callback_query)


# Обработка кнопки изменения ивента
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_'))
async def process_callback_delete(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await edit_event_start(callback_query, state)


# Обработка всех остальных кнопок
@dp.message_handler(Text(equals=["ℹИнформация", '✔Подписки', '🔓Доступные мероприятия']))
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery=None):
    user_id = callback_query.from_user.id
    # Проверка на то, есть ли юзер в бд
    try:
        db.get_any(user_id, 'id')
    except TypeError:
        await callback_query.answer('😬Так.. Смотрю тебя нет в моей базе данных. Пожалуйста, напиши /start для того, чтобы я тебя зарегистрировал)')
        return
    
    await callback(callback_query)




# Запускается при старте программы
async def on_startup(dp):
    # Информация про меня))
    print('')
    print('-------------------------------')
    print('  Скрипт бота тг для итфеста запущен.')
    print('  Разработчик: Кирилл Арзамасцев ')
    print('  GitHub: https://github.com/nickname123456')
    print('  Вк: https://vk.com/kirillarz')
    print('  Дс: CoalNavl#0043')
    print('-------------------------------')
    print('')

    await bot.send_message(admin_id, 'Бот запущен!')

    # Каждые 60 минут запускаем рассылку
    scheduler.add_job(notification, "interval", minutes=60)



# ````````````````````СТАРТ```````````````````````````````````````


# Если запустили этот файл, как главный:
if __name__ == '__main__':
    # Запускаем бота
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)