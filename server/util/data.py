import sqlite3, os

def insert(query: str, values: tuple) -> int:
    db = get_db()
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
    db = get_db()

    cursor = db.cursor()
    cursor.execute(query)
    return get_as_dict(cursor)

def get_db():
    return sqlite3.connect(os.path.join(os.getcwd(),'db','app.db'))


            
def get_as_dict(cursor: sqlite3.Cursor):
    rows = cursor.fetchall() 
    if not rows:
        return None
    return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]






