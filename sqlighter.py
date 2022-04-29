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
                is_admin BIT,
                TechnoCom BIT,
                IT_fest_2022 BIT,
                IASF2022 BIT,
                ФестивальОКК BIT,
                Нейрофест BIT,
                НевидимыйМир BIT,
                КонкурсНИР BIT,
                VRARFest3D BIT
                )""")
        
        # Создаем таблицу со старыми постами
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS old_posts (
                id INT,
                TechnoCom TEXT,
                IT_fest_2022 TEXT,
                IASF2022 TEXT,
                ФестивальОКК TEXT,
                Нейрофест TEXT,
                НевидимыйМир TEXT,
                КонкурсНИР TEXT,
                VRARFest3D TEXT
                )""")



    # Сохраняем изменения в бд
    def commit(self):
        self.connection.commit()




    # Получить старые посты
    def get_old_posts(self, name):
        with self.connection:
            return self.cursor.execute(f'SELECT {name} FROM `old_posts` WHERE `id` = 1').fetchone()[0]
    # Изменить старые посты
    def edit_old_posts(self, name, value):
        with self.connection:
            return self.cursor.execute(f"UPDATE `old_posts` SET {name} = ? WHERE `id` = 1", (str(value),))



    # Получить все про юзера
    def get_all(self, id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `users` WHERE `id` = ?', (id,)).fetchall()[0]



    # Получить что-то по юзера
    def get_any(self, id, name):
        with self.connection:
            return self.cursor.execute(f'SELECT {name} FROM `users` WHERE `id` = {id}').fetchone()[0]
    # Изменить что-то в юзере
    def edit_any(self, id, name,value):
        with self.connection:
            return self.cursor.execute(f"UPDATE `users` SET {name} = {value} WHERE `id` = {id}")



    # Добавить изерв в бд
    def add_user(self, id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?)',(id,0,0,0,0,0,0,0,0,0))



    # Получить пользователей, которые подписаны на ивент
    def get_users_with_notification(self, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `users` WHERE {name} = 1").fetchall()
    

    def add_column(self, name_column, data_type):
        with self.connection:
            return self.cursor.execute(f'ALTER TABLE users ADD COLUMN {name_column} {data_type}')