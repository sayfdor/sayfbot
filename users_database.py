import sqlite3

# users database init
conn = sqlite3.connect('database/users_db.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   user_id INT UNIQUE,
   user_name TEXT,
   user_surname TEXT,
   username TEXT,
   user_lang TEXT,
   user_city TEXT);
""")
conn.commit()

def add_user(user_id: int, user_name: str, user_surname: str, username: str, user_lang: str, user_city: str):
    try:
        add_string = '''REPLACE INTO users (user_id, user_name, user_surname, username, user_lang, user_city)
         VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(add_string, (user_id, user_name, user_surname, username, user_lang, user_city))
        conn.commit()
    except Exception as E:
        print(E)

def search_user(user_id: int) -> bool:
    if list(cursor.execute(f'SELECT EXISTS (SELECT * FROM users WHERE user_id = {user_id})').fetchall()[0])[0] == 1:
        return True
    return False

def get_user_lang(user_id: int) -> str:
    lang = cursor.execute(f"SELECT user_lang FROM users WHERE user_id = {str(user_id)}")
    return str(lang.fetchall()[0][0])

def get_user_city(user_id: int) -> str:
    city = cursor.execute(f"SELECT user_city FROM users WHERE user_id = {str(user_id)}")
    return str(city.fetchall()[0][0])


if __name__ == '__main__':
    pass
