from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    start = State()
    choose = State()
    request_state = State()
