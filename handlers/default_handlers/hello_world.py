from telebot.types import Message
from loader import bot, MyStates


@bot.message_handler(commands=['hello_world'], state=MyStates.start)
def bot_hello_world(message: Message) -> None:
    """
    Отвечает на команду /hello_world
    :param message: сообщение пользователя
    :return: None
    """
    bot.reply_to(message, 'Hello world of telegram!')
