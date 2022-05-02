from sqlighter import SQLighter

db = SQLighter('it_fest.db')

async def start(message):
    try:
        # Если человека нет в бд, добавляем
        if db.get_any(message.from_user.id, 'id') is None:
            db.add_user(message.from_user.id)
    # Если вылезла ошибка, то тоже добавляем
    except TypeError:
        db.add_user(message.from_user.id)
    # Отправляем сообщение
    await message.reply("Привет!\nНапиши мне /menu, чтобы открыть главное меню!")
