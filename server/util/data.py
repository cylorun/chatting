import sqlite3, os


class Data:
    def create_db():
        if not os.path.exists(os.path.join(os.getcwd(),'db','app.db')):
            db = Data.get_db()
            cur = db.cursor()
            cur.execute('''CREATE TABLE images(image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),
                    date INTEGER,
                    user_id INTEGER,
                    channel_id INTEGER,
                    trans BOOLEAN,
                    data BLOB);''')
            cur.execute('''CREATE TABLE channels(channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date INTEGER,
                        name VARCHAR(255),
                        password VARCHAR(255),
                        user_id INTEGER
                        );''')
            cur.execute('''CREATE TABLE messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        channel_id INTEGER,
                        content TEXT,
                        date INTEGER);''')
            cur.execute('''CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),
                    password VARCHAR(255), 
                    email VARCHAR(255),
                    date INTEGER
                    );''')
            db.commit()
            db.close()
    def insert(query: str, values: tuple) -> int:
        db = Data.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(query, values)
            db.commit()
            cursor.close()
            db.close()
            return cursor.lastrowid
        except Exception as e:
            print('errror\n',e)

    def select(query: str):
        db = Data.get_db()

        cursor = db.cursor()
        cursor.execute(query)
        return Data.get_as_dict(cursor)

    def get_db():
        return sqlite3.connect(os.path.join(os.getcwd(),'db','app.db')) # also creates the db file


                
    def get_as_dict(cursor: sqlite3.Cursor):
        rows = cursor.fetchall() 
        if not rows:
            return None
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]






