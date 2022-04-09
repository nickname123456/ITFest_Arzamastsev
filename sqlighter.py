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
                TechnoCom TEXT,
                IT_fest_2022 TEXT,
                IASF2022 TEXT,
                ФестивальОКК TEXT,
                Нейрофест TEXT,
                НевидимыйМир TEXT,
                КонкурсНИР TEXT,
                VRARFest3D TEXT
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
    
    # Получить id
    def get_id(self, id):
        with self.connection:
            return self.cursor.execute('SELECT id FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_TechnoCom(self, id):
        with self.connection:
            return self.cursor.execute('SELECT TechnoCom FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_IT_fest_2022(self, id):
        with self.connection:
            return self.cursor.execute('SELECT IT_fest_2022 FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_IASF2022(self, id):
        with self.connection:
            return self.cursor.execute('SELECT IASF2022 FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_ФестивальОКК(self, id):
        with self.connection:
            return self.cursor.execute('SELECT ФестивальОКК FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_Нейрофест(self, id):
        with self.connection:
            return self.cursor.execute('SELECT Нейрофест FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_НевидимыйМир(self, id):
        with self.connection:
            return self.cursor.execute('SELECT НевидимыйМир FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_КонкурсНИР(self, id):
        with self.connection:
            return self.cursor.execute('SELECT КонкурсНИР FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]
    
    # Получить подписан ли юзер на
    def get_VRARFest3D(self, id):
        with self.connection:
            return self.cursor.execute('SELECT VRARFest3D FROM `users` WHERE `id` = ?', (id,)).fetchone()[0]


    # Добавить изерв в бд
    def add_user(self, id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)',(id,0,0,0,0,0,0,0,0))


    # Изменить что-то в юзере
    def edit_any(self, id, name,value):
        with self.connection:
            return self.cursor.execute(f"UPDATE `users` SET {name} = {value} WHERE `id` = {id}")
    
    # Изменить id в юзере
    def edit_id(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `id` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_TechnoCom(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `TechnoCom` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_IT_fest_2022(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `IT_fest_2022` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_IASF2022(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `IASF2022` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_ФестивальОКК(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `ФестивальОКК` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_Нейрофест(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `Нейрофест` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_НевидимыйМир(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `НевидимыйМир` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_КонкурсНИР(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `КонкурсНИР` = ? WHERE `id` = ?", (value, id))
    
    # Изменить в юзере
    def edit_VRARFest3D(self, id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `VRARFest3D` = ? WHERE `id` = ?", (value, id))



    # Получить пользователей, которые подписаны на ивент
    def get_users_with_notification(self, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `users` WHERE {name} = 1").fetchall()