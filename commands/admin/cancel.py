# Импортируем библиотеки
from aiogram import types
from aiogram.dispatcher import FSMContext

from commands.menu import menu # Импортируем меню

async def cancel(message: types.Message, state: FSMContext):
    await state.finish() # Завершаем действие
    await message.answer("💥Действие отменено")

    await menu(message) # Вызываем меню