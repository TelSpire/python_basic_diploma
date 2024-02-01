import telebot
import config
from commands import commands as cmd
from answer import echo_all as msg


# Создает объект класса Telebot
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['hello_world'])
def commands(message: telebot.types.Message) -> None:
    cmd(message, bot)


@bot.message_handler(func=lambda message: True)
def messages(message: telebot.types.Message) -> None:
    msg(message, bot)


# Запускает бесконечный цикл получения новых записей со стороны Telegram
if __name__ == '__main__':
    bot.infinity_polling()
