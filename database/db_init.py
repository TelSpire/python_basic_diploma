import sqlite3


def init_db() -> None:
    conn = sqlite3.connect('req_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS req_history
                 (user_id INTEGER, query TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()
