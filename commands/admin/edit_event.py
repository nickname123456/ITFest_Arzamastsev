from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlighter import SQLighter
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from private_data import TOKEN_TG
from settings import *

bot = Bot(token=TOKEN_TG)
db = SQLighter('it_fest.db')



class editEventState(StatesGroup):
    name = State()
    link = State()
    hashtag = State()
    description = State()


async def edit_event_kb(message: types.Message):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    kb =InlineKeyboardMarkup(row_width=4)

    events = db.get_all_from_events()
    for event in events:
        kb.insert(InlineKeyboardButton(f'{event[0]}', callback_data=f'edit_{event[0]}'))

    await message.answer('Какой ивент ты хочешь изменить??', reply_markup=kb)


async def edit_event_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await bot.send_message(user_id,'Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return

    data = str(callback_query.data)[5:]

    await editEventState.name.set()
    await state.update_data(old_name=data)

    await bot.send_message(user_id, f'Хочешь изменить {data}? Ну ок. Введи новое название')


async def edit_event_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await state.update_data(name=message.text)
    await editEventState.next()

    await message.answer(f'{message.text}? Отличное название! Теперь введи ссылку на сообщество вк')



async def edit_event_link(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    if not message.text.startswith(tuple('https://vk.com/')):
        await message.answer('Ссылка должна начинаться на "https://vk.com/"!')
        return
    
    await state.update_data(link=message.text)
    await editEventState.next()

    await message.answer(f'{message.text}? Норм паблик! Теперь введи хэштег, если он есть. Если нет, то напиши "нет"')



async def edit_event_hashtag(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    if not message.text.startswith(tuple('#')) and message.text.lower() != 'нет':
        await message.answer('Хэштег должен начинаться на "#"!')
        return
    
    if message.text.lower() == 'нет': 
        await state.update_data(hashtag='')
        await message.answer("Нет хэштега? Ну ничего страшного! Я буду рассылать все посты из указанного паблика. А теперь введи краткое описание ивента")
    else: 
        await state.update_data(hashtag=message.text)
        await message.answer(f"{message.text} ! А че, звучит хайпова. Теперь введи краткое описание ивента")

    await editEventState.next()
    
    



async def edit_event_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    user_data = await state.get_data()


    group_id = user_data['link']
    name = user_data['name']
    old_name = user_data['old_name']
    hashtag = user_data['hashtag']
    description = message.text
    
    db.edit_any_from_events('group_id', old_name, group_id)
    db.edit_any_from_events('hashtag', old_name, hashtag)
    db.edit_any_from_events('description', old_name, description)
    db.edit_any_from_events('name', old_name, name)

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}'))

    await message.answer("Твой ивент успешно обновлен! Хочешь посмотреть?", reply_markup=keyboard)
    await state.finish()
