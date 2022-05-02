async def help(message):
    # Отправляем сообщение
    await message.reply("Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:\nГруппа ВКонтакте Научим.online https://vk.com/nauchim.online\nСайт с мероприятиями https://www.научим.online")
    await message.reply("Вот все мои команды:\n/start - регистрирует вас в базе данных, если вы в ней не зачислены\n/menu - Отправляет главное меню")