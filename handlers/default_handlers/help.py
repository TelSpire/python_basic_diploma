from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot, MyStates


@bot.message_handler(commands=['help'], state=MyStates.start)
def bot_help(message: Message) -> None:
    """
    Выводит доступные команды
    :param message: сообщение пользователя
    :return: None
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
