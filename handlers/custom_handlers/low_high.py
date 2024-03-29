import requests
import json
from telebot.types import Message, ReplyKeyboardRemove
from loader import bot, MyStates, base_request, cache, RA_db
from config_data.config import API_KEY


@bot.message_handler(state=MyStates.start, func=lambda message: message.text in ('Low', 'High'))
def bot_low(message: Message) -> None:
    """
    Выполняет функцию кнопок low и high, переводит в состояние выбора параметров
    :param message: сообщение пользователя
    :return: None
    """
    bot.send_message(message.chat.id, 'Введите через запятую IATA-коды городов отправления и назначения, а также количество выводимых билетов(от 1 до 50)\n'
                                      'Пример: TJM, MOW, 5\n'
                                      'Показывает 5 билетов из Тюмени в Москву', reply_markup=ReplyKeyboardRemove())
    cache[str(message.chat.id)] = {}
    cache[str(message.chat.id)]['sort_type'] = message.text
    bot.set_state(message.from_user.id, MyStates.choose)


@bot.message_handler(state=MyStates.choose, func=lambda message: True)
def bot_low_choose(message: Message) -> None:
    """
    Сохраняет параметры и запрашивает по какому параметру фильтровать
    :param message: сообщение от пользователя
    :return: None
    """
    cache[str(message.chat.id)]['low_request'] = dict(base_request)
    low_request = cache[str(message.chat.id)]['low_request']
    data = message.text.split(', ')
    if len(data) != 3:
        bot.reply_to(message, 'Введено недостаточно данных либо не верный синтаксис, попробуйте снова!')
        return None
    low_request['origin'] = data[0]
    low_request['destination'] = data[1]
    if 1 <= int(data[2]) <= 50:
        low_request['amount'] = int(data[2])
    else:
        low_request['amount'] = 50
    bot.send_message(message.chat.id, 'Введите по какому параметру отфильтровать билеты:\n'
                     'Цена, дата или длительность')
    bot.set_state(message.from_user.id, MyStates.request_state, message.chat.id)


@bot.message_handler(state=MyStates.request_state, func=lambda message: True)
def bot_low_request(message: Message) -> None:
    """
    Выводит билеты по заданным параметрам, типу фильтрации и по типу запроса
    :param message: сообщение пользователя
    :return: None
    """
    msg = message.text.lower()
    low_request = cache[str(message.chat.id)]['low_request']
    if msg in ('цена', 'дата', 'длительность'):
        bot.send_message(message.chat.id, 'По вашему запросу были найдены билеты:')
        action = {'цена': 'value', 'дата': 'depart_date', 'длительность': 'duration'}
        req_url = f'https://api.travelpayouts.com/v2/prices/month-matrix?currency=rub&origin={low_request['origin']}&destination={low_request['destination']}&show_to_affiliates=true&limit={low_request['amount']}&token={API_KEY}'
        response = requests.get(req_url).text
        req_data = json.loads(response)
        answer = [f'Билет {i+1} \nЦена: {ticket['value']} \nДата отправления: {ticket['depart_date']} \nДлительность полета в минутах: {ticket['duration']} \nКомпания: {ticket['gate']}' for i, ticket in enumerate(sorted(req_data['data'], key=lambda x: x[action[msg]], reverse=cache[str(message.chat.id)]['sort_type'] == 'High'))][0:low_request['amount']]
        for i_ticket in answer:
            bot.send_message(message.chat.id, i_ticket)
        bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
        user_cache = cache[str(message.chat.id)]
        RA_db.add_user_query(message.chat.id, f"Тип: {user_cache['sort_type']} \nМесто отправления, назначение и количество: {low_request['origin']}, {low_request['destination']}, {low_request['amount']} \nПараметр фильтрации: {msg}\n")
        cache[str(message.chat.id)] = {}
    else:
        bot.send_message(message.chat.id, 'Введен не существующий фильтр')
