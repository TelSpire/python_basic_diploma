from telebot.types import Message
from loader import bot, MyStates


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None, func=lambda message: True)
def bot_echo(message: Message) -> None:
    """
    Отвечает на все сообщение не попавшие в другие фильтры
    :param message: сообщение пользователя
    :return: None
    """
    bot.reply_to(
        message,
        'Эхо без состояния или фильтра.\n' 
        f'Сообщение: {message.text}'
    )
    bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
