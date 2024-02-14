from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """
    Класс со всеми состояниями
    """
    start = State()
    choose = State()
    request_state = State()
    choose_custom = State()
    request_state_custom = State()
