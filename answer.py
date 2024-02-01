import telebot


def echo_all(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """
    Отвечает на все сообшения, если написали привет, то выдает список комманд
    :param message: Сообщение пользователя
    :param bot: Объект бота
    :return: None
    """
    if 'привет' in message.text.lower():
        bot.reply_to(message, 'Здравствуй пользователь!\n'
                              'Список доступных комманд:\n'
                              '/hello_world - Выводит "Hello World!"')
    else:
        bot.reply_to(message, message.text)
