from telebot.types import Message
from loader import bot, MyStates


@bot.message_handler(func=lambda message: 'привет' in message.text.lower() or message.text == '/start')
def bot_hello(message: Message) -> None:
    """
    Переводит в состояние старт и подсказывает дальнейшие действия
    :param message: сообщение пользователя
    :return: None
    """
    bot.reply_to(message, f'Здравствуй {message.from_user.full_name}!\n'
                          'Чтобы узнать все доступные комманды введите /help')
    bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
