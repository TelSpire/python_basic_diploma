from loader import bot, MyStates
from telebot import types


@bot.message_handler(state=MyStates.start, commands=['menu'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_low = types.KeyboardButton("Low")
    btn_high = types.KeyboardButton("High")
    # item3 = types.KeyboardButton("Custom")
    markup.add(btn_low, btn_high)
    bot.reply_to(message, "Выберите кнопку:", reply_markup=markup)
