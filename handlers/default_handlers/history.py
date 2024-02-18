from telebot.types import Message
from loader import bot, MyStates, RA_db
import sqlite3


@bot.message_handler(commands=['history'], state=MyStates.start)
def history_command(message: Message) -> None:
    """
    Выводит 10 последних запросов пользователя
    :param message: сообщение пользователя
    :return: None
    """
    bot.send_message(message.chat.id, 'История 10 последних запросов:')
    reqs = RA_db.read_user_query(message.chat.id)
    if len(reqs) > 0:
        bot.send_message(message.chat.id, reqs)
    else:
        bot.send_message(message.chat.id, 'История пуста!')
