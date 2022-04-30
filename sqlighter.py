# Импортируем sqlite3
import sqlite3

# Создаем класс
class SQLighter:
    # При объявление класса
    def __init__(self, db):
        # Подключаемся к бд
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        # Создаем таблицу с юзерами
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
                id INT,
                is_admin BIT
                )""")


        # Создаем таблицу со старыми постами
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events (
                name TEXT,
                group_id TEXT,
                hashtag TEXT,
                old_posts TEXT,
                users TEXT
                )""")



    # Сохраняем изменения в бд
    def commit(self):
        self.connection.commit()



    # Получить все про юзера
    def get_all(self, id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `users` WHERE `id` = ?', (id,)).fetchall()[0]
    
    def get_all_from_events(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `events`').fetchall()



    # Получить пользователей, которые подписаны на ивент
    def get_users_with_notification(self, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `users` WHERE {name} = 1").fetchall()



    # Получить что-то по юзера
    def get_any(self, id, name):
        with self.connection:
            return self.cursor.execute(f'SELECT {name} FROM `users` WHERE `id` = {id}').fetchone()[0]
    # Изменить что-то в юзере
    def edit_any(self, id, name,value):
        with self.connection:
            return self.cursor.execute(f"UPDATE `users` SET {name} = {value} WHERE `id` = {id}")
    


    def get_any_from_events(self, column, name):
        with self.connection:
            return self.cursor.execute(f'SELECT {column} FROM `events` WHERE `name` = ?', (name,)).fetchone()[0]
    
    def edit_any_from_events(self, column, name, value):
        with self.connection:
            return self.cursor.execute(f"UPDATE `events` SET {column} = ? WHERE `name` = ?", (value, name,))



    # Добавить изерв в бд
    def add_user(self, id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users VALUES (?,?)',(id,0))
    
    def add_event(self, name, group_id, hashtag):
            with self.connection:
                return self.cursor.execute('INSERT INTO events VALUES (?,?,?,?,?)',(name, group_id, hashtag, '[]', '[]'))

    def add_column(self, table, name_column, data_type):
        with self.connection:
            return self.cursor.execute(f'ALTER TABLE {table} ADD COLUMN {name_column} {data_type}')

