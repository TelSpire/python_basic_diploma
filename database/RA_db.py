import sqlite3


def add_user_query(user_id: int, query: str) -> None:
    """
    Сохраняет запрос пользователя в базу данных, но не более 10, при переполнении удаляет самый старый запрос
    :param user_id: id пользователя
    :param query: запрос
    :return: None
    """
    conn = sqlite3.connect('req_history.db')
    c = conn.cursor()
    c.execute('''INSERT INTO req_history (user_id, query, timestamp)
                 VALUES (?, ?, CURRENT_TIMESTAMP)''', (user_id, query))
    conn.commit()

    c.execute('''DELETE FROM req_history WHERE user_id = ? AND timestamp NOT IN
                 (SELECT timestamp FROM req_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10)''',
              (user_id, user_id))
    conn.commit()
    conn.close()


def read_user_query(user_id: int) -> str:
    """
    Считывает историю запросов пользователя из базы данных
    :param user_id: id пользователя
    :return: 10 последних запросов пользователя в формате строки
    """
    conn = sqlite3.connect('req_history.db')
    c = conn.cursor()
    c.execute('''SELECT query FROM req_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10''',
              (user_id,))
    rows = c.fetchall()
    conn.close()
    reqs = '\n'.join([row[0] for row in rows])
    return reqs
