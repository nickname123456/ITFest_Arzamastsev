# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PostgreSQLighter import SQLighter
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from private_data import TOKEN_TG
from settings import *

bot = Bot(token=TOKEN_TG)
db = SQLighter('it_fest.db') # Подключение к бд


# Создаем стейты
class editEventState(StatesGroup):
    name = State()
    link = State()
    hashtag = State()
    description = State()


async def edit_event_kb(message: types.Message):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    
    kb =InlineKeyboardMarkup(row_width=4)
    # Перебираем все ивенты
    events = db.get_all_from_events()
    for event in events:
        kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'edit_{event[0]}'))

    await bot.send_message(user_id, '🧐Какой ивент ты хочешь изменить??', reply_markup=kb)


async def edit_event_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await bot.send_message(user_id,'⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return

    data = str(callback_query.data)[5:]

    # Проверка, есть ли вообще ивент в бд
    try:
        db.get_any_from_events('name', data)
    except TypeError:
        await bot.edit_message_text('🫠Прости, но кажется этого ивента у меня нет в базе данных. Возможно его удалили', user_id, callback_query.message.message_id) # Редактируем старое сообщение
        return

    await editEventState.name.set() # Задаем стейт
    await state.update_data(old_name=data) # Задаем старое название

    keyboard = (
            InlineKeyboardMarkup()
            .add(InlineKeyboardButton('Оставить прежнее название', callback_data=f'edit_keep_name'))
        )

    await bot.send_message(user_id, f'😲Хочешь изменить {data}? Ну ок. Введи новое название', reply_markup=keyboard)


async def edit_event_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    if len(message.text) > 35:
        await message.answer('⛔Слишком большое название! Пожалуйста, попробуй его сократить')
        return
    
    await state.update_data(name=message.text) # Задаем новое название
    await editEventState.next() # Переходим на следующий этап

    keyboard = (
            InlineKeyboardMarkup()
            .add(InlineKeyboardButton('Оставить прежнию ссылку', callback_data=f'edit_keep_link'))
        )

    await message.answer(f'✅{message.text}? Отличное название! Теперь введи ссылку на сообщество вк', reply_markup=keyboard)



async def edit_event_link(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    # Если ссылка не вк
    if not message.text.startswith(tuple('https://vk.com/')):
        await message.answer('❌Ссылка должна начинаться на "https://vk.com/"!')
        return
    
    await state.update_data(link=message.text) # Задаем новую ссылку
    await editEventState.next() # Переходим на следующий этап

    keyboard = (
            InlineKeyboardMarkup()
            .add(InlineKeyboardButton('Оставить прежний хэштег', callback_data=f'edit_keep_hashtag'))
        )

    await message.answer(f'✅{message.text}? Норм паблик! Теперь введи хэштег, если он есть. Если нет, то напиши "нет"', reply_markup=keyboard)



async def edit_event_hashtag(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    # Если неправильный хэштег
    if not message.text.startswith(tuple('#')) and message.text.lower() != 'нет':
        await message.answer('❌Хэштег должен начинаться на "#"!')
        return
    
    keyboard = (
            InlineKeyboardMarkup()
            .add(InlineKeyboardButton('Оставить прежнее описание', callback_data=f'edit_keep_description'))
        )

    if message.text.lower() == 'нет': # Если нет хэштега
        await state.update_data(hashtag='')
        await message.answer("🫡Нет хэштега? Ну ничего страшного! Я буду рассылать все посты из указанного паблика. А теперь введи краткое описание ивента", reply_markup=keyboard)
    else: # Если есть хэштег
        await state.update_data(hashtag=message.text)
        await message.answer(f"✅{message.text} ! А че, звучит хайпова. Теперь введи краткое описание ивента", reply_markup=keyboard)

    await editEventState.next() # Переходим на следующий этап
    
    



async def edit_event_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await state.update_data(description=message.text)
    
    user_data = await state.get_data() # Получаем все новые данные
    old_name = user_data['old_name'] # Старое название

    if user_data['link'] == 'keep_old': group_id = db.get_any_from_events('group_id',old_name) # Если надо оставить старую ссылку
    else: group_id = user_data['link'] # Если не надо оставить старую ссылку

    if user_data['name'] == 'keep_old': name = db.get_any_from_events('name',old_name)
    else: name = user_data['name']
    
    if user_data['hashtag'] == 'keep_old': hashtag = db.get_any_from_events('hashtag',old_name)
    else: hashtag = user_data['hashtag']
    
    if user_data['description'] == 'keep_old': description = db.get_any_from_events('description',old_name)
    else: description = user_data['description']
    
    # Меняем значения в бд
    db.edit_any_from_events('group_id', old_name, group_id)
    db.edit_any_from_events('hashtag', old_name, hashtag)
    db.edit_any_from_events('description', old_name, description)
    db.edit_any_from_events('name', old_name, name)

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}'))

    await message.answer("✅Твой ивент успешно обновлен! Хочешь посмотреть?", reply_markup=keyboard)
    await state.finish() # Завершаем