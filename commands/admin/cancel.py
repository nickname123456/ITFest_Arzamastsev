from aiogram import types
from aiogram.dispatcher import FSMContext

from commands.menu import menu

async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")

    await menu(message)