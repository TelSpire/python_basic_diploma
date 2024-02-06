import requests
import json
from telebot.types import Message, ReplyKeyboardRemove
from loader import bot, MyStates, bot_type, base_request
from config_data.config import API_KEY


@bot.message_handler(func=lambda message: message.text in ('Low', 'High'), state=MyStates.start)
def bot_low(message: Message) -> None:
    global bot_type
    bot.send_message(message.chat.id, 'Введите через запятую IATA-коды городов отправления и назначения, а также количество выводимых билетов(от 1 до 30)\n'
                                      'Пример: TJM, MOW, 5\n'
                                      'Показывает 5 билетов из Тюмени в Москву', reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, MyStates.choose, message.chat.id)
    bot_type = message.text


@bot.message_handler(func=lambda x: bot_type in ('Low', 'High'), state=MyStates.choose)
def bot_low_choose(message: Message) -> None:
    global low_request, bot_type
    low_request = dict(base_request)
    data = message.text.split(', ')
    if len(data) != 3:
        bot.reply_to(message, 'Введено недостаточно данных либо не верный синтаксис, попробуйте снова!')
        return None
    low_request['origin'] = data[0]
    low_request['destination'] = data[1]
    if 1 <= int(data[2]) <= 30:
        low_request['amount'] = int(data[2])
    else:
        low_request['amount'] = 30
    bot.send_message(message.chat.id,
                     'Введите по какому параметру отфильтровать билеты:\n'
                     'Цена, дата или длительность')  # (Время между прилетом в место назначения и отбытием обратно)
    bot.set_state(message.from_user.id, MyStates.request_state, message.chat.id)


@bot.message_handler(func=lambda x: bot_type in ('Low', 'High'), state=MyStates.request_state)
def bot_low_choose(message: Message) -> None:
    global bot_type, low_request
    msg = message.text.lower()
    if msg in ('цена', 'дата', 'длительность'):
        action = {'цена': 'value', 'дата': 'depart_date', 'длительность': 'duration'}
        req_url = f'https://api.travelpayouts.com/v2/prices/month-matrix?currency=rub&origin={low_request['origin']}&destination={low_request['destination']}&show_to_affiliates=true&token={API_KEY}'
        response = requests.get(req_url).text
        req_data = json.loads(response)
        answer = '\n'.join([f'Билет {i+1} \n Цена: {ticket['value']} \nДата отправления: {ticket['depart_date']} \nДлительность: {ticket['duration']}\n' for i, ticket in enumerate(sorted(req_data['data'], key=lambda x: x[action[msg]], reverse=bot_type == 'High'))][0:low_request['amount']])
        bot.send_message(message.chat.id, 'По вашему запросу были найдены билеты:\n'
                                          f'{answer}')
        bot_type = None
        bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Введен не существующий фильтр')
