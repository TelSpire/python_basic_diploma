import telebot


def commands(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """
    Выполняет запрошенные команды
    :param bot: Объект бота
    :param message: Сообщение с командой
    :return: None
    """
    if message.text == '/hello_world':
        bot.reply_to(message, 'Hello world!')
    else:
        bot.reply_to(message, 'Неизвестная команда!')