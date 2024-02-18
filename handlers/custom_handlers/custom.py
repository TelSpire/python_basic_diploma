import requests
import json
from telebot.types import Message, ReplyKeyboardRemove
from loader import bot, MyStates, base_request, cache, RA_db
from config_data.config import API_KEY


def filter_for_custom(ticket: dict, message: Message) -> bool:
    """
    Фильтрует билеты по заданным настройкам
    :param ticket: Билет
    :param message: Сообщение пользователя
    :return: True если билет подходит по параметрам, Else В ином случае
    """
    params = cache[str(message.chat.id)]['settings']
    if (
            params['цена'][0] <= ticket['value'] <= params['цена'][1] and
            params['дата'][0] <= int(ticket['depart_date'][-2:]) <= params['дата'][1] and
            params['длительность'][0] <= ticket['duration'] <= params['длительность'][1]
    ):
        return True
    else:
        return False


def save_values(message: Message, parameter: str) -> None:
    """
    Сохраняет настройки для данного параметра
    :param message: сообщение пользователя
    :param parameter: параметр
    :return: None
    """
    value = list(map(int, message.text.split()))
    cache[str(message.chat.id)]['settings'][parameter] = value
    bot.send_message(message.chat.id, 'Введите какой параметр настроить:\n'
                     'Цена, дата или длительность\n'
                     'Либо введите "Результат" чтобы вывести найденные билеты')


@bot.message_handler(state=MyStates.start, func=lambda message: message.text == 'Custom')
def bot_custom(message: Message) -> None:
    """
    Выполняет действие кнопки Custom, переводит в состояние выбора настроек
    :param message: сообщение пользователя
    :return: None
    """
    bot.send_message(message.chat.id, 'Введите через запятую IATA-коды городов отправления и назначения, а также количество выводимых билетов(от 1 до 50)\n'
                                      'Пример: TJM, MOW\n'
                                      'Показывает найденные билеты из Тюмени в Москву', reply_markup=ReplyKeyboardRemove())
    cache[str(message.chat.id)] = {}
    cache[str(message.chat.id)]['settings'] = {'цена': [0, 1000000], 'дата': [0, 31], 'длительность': [0, 2880]}
    bot.set_state(message.from_user.id, MyStates.choose_custom)


@bot.message_handler(state=MyStates.choose_custom, func=lambda message: True)
def bot_custom_choose(message: Message) -> None:
    """
    Сохраняет настройки для поиска в кэш
    :param message: сообщение пользователя
    :return: None
    """
    cache[str(message.chat.id)]['low_request'] = dict(base_request)
    low_request = cache[str(message.chat.id)]['low_request']
    data = message.text.split(', ')
    if len(data) != 2:
        bot.reply_to(message, 'Введено недостаточно данных либо не верный синтаксис, попробуйте снова!')
        return None
    low_request['origin'] = data[0]
    low_request['destination'] = data[1]
    low_request['amount'] = 50
    bot.send_message(message.chat.id, 'Введите какой параметр настроить:\n'
                     'Цена, дата или длительность\n'
                     'Либо введите "Результат" чтобы вывести найденные билеты')
    bot.set_state(message.from_user.id, MyStates.request_state_custom, message.chat.id)


@bot.message_handler(state=MyStates.request_state_custom, func=lambda message: True)
def bot_custom_request(message: Message) -> None:
    """
    Запрашивает настройки для фильтра, либо отправляет запрос к API и выводит результаты поиска
    :param message: сообщение пользователя
    :return: None
    """
    msg = message.text.lower()
    low_request = cache[str(message.chat.id)]['low_request']
    if msg in ('цена', 'дата', 'длительность'):
        bot.send_message(message.chat.id, f'Введите максимальное и минимальное значение через пробел для параметра "{msg}"\n'
                                          'Например: 5 30\n'
                                          'Лимиты: цена - 1.000.000, дата - 31, длительность - 2880 минут (2 дня)')
        bot.register_next_step_handler(message, save_values, msg)
    elif msg == 'результат':
        bot.send_message(message.chat.id, 'По вашему запросу были найдены билеты:')
        req_url = f'https://api.travelpayouts.com/v2/prices/month-matrix?currency=rub&origin={low_request['origin']}&destination={low_request['destination']}&show_to_affiliates=true&limit={low_request['amount']}&token={API_KEY}'
        response = requests.get(req_url).text
        req_data = json.loads(response)
        answer = [f'Билет {i + 1} \nЦена: {ticket['value']} \nДата отправления: {ticket['depart_date']} \nДлительность полета в минутах: {ticket['duration']} \nКомпания: {ticket['gate']}' for i, ticket in enumerate(filter(lambda ticket: filter_for_custom(ticket, message), req_data['data']))]
        if len(answer) == 0:
            bot.send_message(message.chat.id, 'Не найдено билетов по вашему запросу')
        else:
            for i_ticket in answer:
                bot.send_message(message.chat.id, i_ticket)
        bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
        user_cache = cache[str(message.chat.id)]['settings']
        RA_db.add_user_query(message.chat.id, f"Тип: Custom \nМесто отправления, назначение: {low_request['origin']}, {low_request['destination']} \nПараметр фильтрации: Цена {user_cache['цена']}, Дата {user_cache['дата']}, Длительность {user_cache['длительность']}\n")
        cache[str(message.chat.id)] = {}
    else:
        bot.send_message(message.chat.id, 'Введен не существующий фильтр')
