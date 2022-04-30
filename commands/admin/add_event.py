# Импортируем библиотеки
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlighter import SQLighter
import random
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from settings import *
from private_data import TOKEN_TG
import keyboard


scheduler = AsyncIOScheduler()
# Инициализируем бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
# Подключаемся бота
db = SQLighter('it_fest.db')



class addEventState(StatesGroup):
    name = State()
    link = State()
    hashtag = State()



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

    await message.answer(f'{message.text}? Норм паблик! Теперь введи хэштег, если он есть. Если нет, то нажми на кнопку ниже')



async def add_event_hashtag(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    if not message.text.startswith(tuple('#')):
        await message.answer('Хэштег должен начинаться на "#"!')
        return
    
    user_data = await state.get_data()
    
    await message.answer(f"{user_data['name']} {user_data['link']} {message.text}")
    await state.finish()