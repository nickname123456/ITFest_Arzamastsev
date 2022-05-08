import psycopg2
from private_data import DATABASE_URL



# Создаем класс
class SQLighter:
    # При объявление класса
    def __init__(self, db):
        # Подключаемся к бд
        self.connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cursor = self.connection.cursor()
        # Создаем таблицу с юзерами
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
                id INT,
                is_admin INT
                )""")


        # Создаем таблицу со старыми постами
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events (
                name TEXT,
                group_id TEXT,
                hashtag TEXT,
                description TEXT,
                old_posts TEXT,
                users TEXT
                )""")

        self.connection.commit()



    # Сохраняем изменения в бд
    def commit(self):
        self.connection.commit()


    # Получить все про юзера
    def get_all(self, id):
        self.cursor.execute(f'SELECT * FROM users WHERE id = {id}')
        return self.cursor.fetchall()
    
    # Получить все ивенты
    def get_all_from_events(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM events')
            return self.cursor.fetchall()



    # Получить пользователей, которые подписаны на ивент
    def get_users_with_notification(self, name):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users WHERE {name} = 1")
            return self.cursor.fetchall()



    # Получить что-то про юзера
    def get_any(self, id, name):
        with self.connection:
            self.cursor.execute(f'SELECT {name} FROM users WHERE id = %s', (id,))
            return self.cursor.fetchone()[0]
    # Изменить что-то в юзере
    def edit_any(self, id, name,value):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET {name} = %s WHERE id = %s", (value, id,))
            return self.cursor
    

    # Получить что-то из ивентов
    def get_any_from_events(self, column, name):
        with self.connection:
            self.cursor.execute(f'SELECT {column} FROM events WHERE name = %s', (name,))
            return self.cursor.fetchone()[0]
    # Изменить что-то из ивентов
    def edit_any_from_events(self, column, name, value):
        with self.connection:
            self.cursor.execute(f"UPDATE events SET {column} = %s WHERE name = %s", (value, name,))
            return self.cursor



    # Добавить юзера в бд
    def add_user(self, id):
        with self.connection:
            self.cursor.execute('INSERT INTO users VALUES (%s,%s)', (id, 0,))
            return self.cursor
    # Добавить ивент
    def add_event(self, name, group_id, hashtag, description):
            with self.connection:
                self.cursor.execute('INSERT INTO events VALUES (%s,%s,%s,%s,%s,%s)', (name, group_id, hashtag, description,'[]','[]'))
                return self.cursor
    # Добавить колонну
    def add_column(self, table, name_column, data_type):
        with self.connection:
            self.cursor.execute(f'ALTER TABLE {table} ADD COLUMN {name_column} {data_type}')
            return self.cursor


    # Удалить что-то из ивентов
    def delete_any_from_events(self, name):
        with self.connection:
            self.cursor.execute(f'DELETE FROM events WHERE name = (%s)', (name,))
            return self.cursor