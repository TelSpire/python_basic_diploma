from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: 'привет' in message.text.lower())
def bot_hello(message: Message) -> None:
    bot.reply_to(message, f'Здравствуй {message.from_user.full_name}!\n'
                          'Чтобы узнать все доступные комманды введите /help')
