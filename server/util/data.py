import sqlite3, os
class Data:
    def __init__(self):
        self.data = {}
    
    def load(self):
        db = self.get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM users')
        self.data['users'] = self.get_as_dict(cursor)
        
        cursor.execute('SELECT * FROM messages')
        self.data['messages'] = self.get_as_dict(cursor)
        
        cursor.close()
        db.close()
        
        return self.data

    def insert(self, query: str, values: tuple) -> bool:
        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(query, values)
            db.commit()
            cursor.close()
            db.close()
            
            return True
        except Exception as e:
            print(e)
            return False
    def select(self, query: str):
        db = self.get_db()
    
        cursor = db.cursor()
        cursor.execute(query)

        return self.get_as_dict(cursor)
        
    def get_db(self):
        return sqlite3.connect(os.path.join(os.getcwd(),'db','app.db'))
    
    @staticmethod
    def user_from_id(self, user_id):
            for user in self.data['users']:
                if user_id == user['user_id']:
                    return user
                
            return {"date":	None,
                    "email"	:"demo@demo.com",
                    "name"	:"demo",
                    "password	":"demo",
                    "user_id"	:"0"}
                
    @staticmethod
    def get_as_dict(cursor):
        d = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return d





