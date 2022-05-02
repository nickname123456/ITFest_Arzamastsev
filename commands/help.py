from sqlighter import SQLighter
db = SQLighter('it_fest.db')

async def help(message):
    # Отправляем сообщение
    await message.answer("Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:\nГруппа ВКонтакте Научим.online https://vk.com/nauchim.online\nСайт с мероприятиями https://www.научим.online")
    await message.answer("Вот все мои команды:\n/start - регистрирует вас в базе данных, если вы в ней не зачислены\n/menu - Отправляет главное меню")

    if db.get_any(message.from_user.id, 'is_admin') == 1:
        await message.answer("Специально для администраторов (только никому не говори): \n/add - добавить новый ивент \n/edit - изменить существующий ивент \n/delete - удалить ивент")