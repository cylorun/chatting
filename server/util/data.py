import sqlite3, os


class Data:
    def __init__(self):
        self.data = {}
    

    def insert(self, query: str, values: tuple) -> int:
        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(query, values)
            db.commit()
            cursor.close()
            db.close()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def select(self, query: str):
        db = self.get_db()
    
        cursor = db.cursor()
        cursor.execute(query)
        return self.get_as_dict(cursor)
    
    @staticmethod
    def get_db():
        return sqlite3.connect(os.path.join(os.getcwd(),'db','app.db'))
    

                
    @staticmethod
    def get_as_dict(cursor):
        rows = cursor.fetchall() 
        if not rows:
            return None
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]






