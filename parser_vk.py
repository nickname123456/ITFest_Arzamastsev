# импортируем библиотеки
from vkbottle import API
from settings import *
from private_data import TOKEN_VK
import datetime

# Получение постов по id сообщества и хэштэгу
async def get_wall(owner_id, hashtag):
    # Подключаемся к вк
    api = API(TOKEN_VK)
    # Получаем стену вк
    wall = await api.wall.get(owner_id=owner_id)
    # Результат = []
    result = []
    # Перебираем стену
    for i in wall.items[:5]:
        # Если в посте есть наш хэштег, то записываем текст поста в переменную результат
        if hashtag in str(i.text):
            date = i.date
            date = datetime.datetime.fromtimestamp(date)
            date = date.strftime('%Y-%m-%d %H:%M:%S')

            result.append(f"⚠️Новый пост⚠️\n📆Дата: {date} \n🗓️Текст: \n{i.text}")
        
    # Возвращаяем результат
    return result


# Получение всех постов и новых
async def get_notification(hashtag, link, old_posts):
    screen_name = str(link)[15:]
    owner_id = await get_id(screen_name)
    all_posts = await get_wall(owner_id, hashtag)

    # Получаем новые посты
    new_posts = []
    # Перебираем все посты
    for post in all_posts:
        # Если поста нет в бд
        if post not in eval(old_posts):
            # Добавляем пост в новые посты
            new_posts.append(post)
    
    # Возвращаем все посты и новые
    return all_posts, new_posts


async def get_id(screen_name):
    # Подключаемся к вк
    api = API(TOKEN_VK)
    info = await api.utils.resolve_screen_name(screen_name)

    if info.type.value: return -abs(info.object_id)
    else: return info.object_id