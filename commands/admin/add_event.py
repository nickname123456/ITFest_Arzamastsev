# Импортируем библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PostgreSQLighter import SQLighter
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random

from settings import *
from private_data import TOKEN_TG

# Подключение к бд
db = SQLighter('it_fest.db')
# Инициализируем бота
bot = Bot(token=TOKEN_TG)


# Создаем стейты
class addEventState(StatesGroup):
    name = State()
    link = State()
    hashtag = State()
    description = State()



async def add_event_start(message: types.Message):
    user_id = message.from_user.id
    
    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    
    await bot.send_message(user_id, '👀Новый ивент? Это хорошо! Введи название')
    await addEventState.name.set() # Задаем стейт


async def add_event_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    if len(message.text) > 35:
        await message.answer('❌Слишком большое название! Пожалуйста, попробуй его сократить')
        return

    await state.update_data(name=message.text) # Задаем новое название
    await addEventState.next() # Переходим на следующий этап

    await message.answer(f'✅{message.text}? Отличное название! Теперь введи ссылку на сообщество вк')



async def add_event_link(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    # Если пользователь отправил не ссылку вк
    if not message.text.startswith('https://vk.com/'):
        await message.answer('❌Ссылка должна начинаться на "https://vk.com/"!')
        return
    
    await state.update_data(link=message.text) # Задаем новую ссылку
    await addEventState.next() # Переходим на следующий этап

    keyboard = (
            InlineKeyboardMarkup()
            .add(InlineKeyboardButton('Нет хэштега', callback_data=f'add_non_hashtag'))
        )

    await message.answer(f'✅{message.text}? Норм паблик! Теперь введи хэштег, если он есть. Если нет, то нажми на кнопку ниже', reply_markup=keyboard)



async def add_event_hashtag(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('⛔Это команда доступна только администраторам!⛔ \n Если хочешь им стать, обратись к @Momfj')
        return
    # Если неправильный хэштег
    if not message.text.startswith(tuple('#')) and message.text.lower() != 'нет':
        await message.answer('❌Хэштег должен начинаться на "#"!')
        return
    
    # Если нет хэштега
    if message.text.lower() == 'нет': 
        await state.update_data(hashtag='')
        await message.answer("😲Нет хэштега? Ну ничего страшного! Я буду рассылать все посты из указанного паблика. А теперь введи краткое описание ивента")
    else: 
        await state.update_data(hashtag=message.text) # Задаем новый хэштег
        await message.answer(f"✅{message.text} ! А че, звучит хайпова. Теперь введи краткое описание ивента")

    await addEventState.next() # Переходим на следующий этап
    
    



async def add_event_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверка на то, является ли юзер админом
    if db.get_any(user_id, 'is_admin') == 0:
        await message.answer('Это команда доступна только администраторам! \n Если хочешь им стать, обратись к @Momfj')
        return
    
    user_data = await state.get_data() # Получаем все новые данные


    group_id = user_data['link']
    name = user_data['name']
    hashtag = user_data['hashtag']
    description = message.text
    
    db.add_event(name, group_id, hashtag, description) # Добавляем новый ивент

    keyboard = (
        InlineKeyboardMarkup()
        .add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}'))
        .add(InlineKeyboardButton('Добавить еще ивент', callback_data=f'add_event'))
        )

    await message.answer("✅✅Твой ивент успешно добавлен! Хочешь посмотреть?", reply_markup=keyboard)
    await state.finish() # Завершаем

    for user in db.get_all():
        await bot.send_message(user[0], 
            f'{random.choice(smiles)}{random.choice(greetings)}! Уважаемая Администрация добавила новый ивент! Хочешь посмотреть?', 
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'{name}', callback_data=f'info_{name}')))