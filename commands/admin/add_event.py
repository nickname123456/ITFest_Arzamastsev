from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlighter import SQLighter
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from settings import *


db = SQLighter('it_fest.db')



class addEventState(StatesGroup):
    name = State()
    link = State()
    hashtag = State()
    description = State()



async def add_event_start(message: types.Message):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await message.answer('Новый ивент? Это хорошо! Введи название')
    await addEventState.name.set()


async def add_event_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await state.update_data(name=message.text)
    await addEventState.next()

    await message.answer(f'{message.text}? Отличное название! Теперь введи ссылку на сообщество вк')



async def add_event_link(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    if not message.text.startswith(tuple('https://vk.com/')):
        await message.answer('Ссылка должна начинаться на "https://vk.com/"!')
        return
    
    await state.update_data(link=message.text)
    await addEventState.next()

    await message.answer(f'{message.text}? Норм паблик! Теперь введи хэштег, если он есть. Если нет, то напиши "нет"')



async def add_event_hashtag(message: types.Message, state: FSMContext):
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

    await addEventState.next()
    
    



async def add_event_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    user_data = await state.get_data()


    group_id = user_data['link']
    name = user_data['name']
    hashtag = user_data['hashtag']
    description = message.text
    
    db.add_event(name, group_id, hashtag, description)

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}'))

    await message.answer("Твой ивент успешно добавлен! Хочешь посмотреть?", reply_markup=keyboard)
    await state.finish()
