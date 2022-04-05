import sqlite3

# users database init
conn = sqlite3.connect('database/users_db.db', check_same_thread=False)
cursor = conn.cursor()

def add_user(user_id: int, user_name: str, user_surname: str, username: str, user_lang: str):
    try:
        add_string = 'REPLACE INTO users (user_id, user_name, user_surname, username, user_lang) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(add_string, (user_id, user_name, user_surname, username, user_lang))
        conn.commit()
    except Exception as E:
        print(E)

def search_user(user_id: int) -> bool:
    if list(cursor.execute(f'SELECT EXISTS (SELECT * FROM users WHERE user_id = {user_id})').fetchall()[0])[0] == 1:
        return True
    return False

def get_user_lang(user_id: int) -> str:
    lang = cursor.execute(f"SELECT user_lang FROM users WHERE user_id = {str(user_id)}")
    return lang.fetchall()[0][0]


if __name__ == '__main__':
    pass
