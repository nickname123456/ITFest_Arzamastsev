# импортируем библиотеки
from vkbottle import API
from settings import *

# Получение постов по id сообщества и хэштэгу
async def get_wall(owner_id, hashtag):
    # Подключаемся к вк
    api = API("e2ada8c4e2ada8c4e2ada8c47de2d65c91ee2ade2ada8c480eb5de7e19e16f89bf20ca0")
    # Получаем стену вк
    wall = await api.wall.get(owner_id=owner_id)
    # Результат = []
    result = []
    # Перебираем стену
    for i in wall.items:
        # Если в посте есть наш хэштег, то записываем текст поста в переменную результат
        if hashtag in str(i.text):
            result.append(f"Новый пост\n{i.text}")
        
    # Возвращаяем результат
    return result


# Получение всех постов и новых
async def get_notification(event, old_posts):
    # Получаем все посты с этим хэштегом
    all_posts = await get_wall(int(event[2]), hashtags_and_abbreviations[event[1]])

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


