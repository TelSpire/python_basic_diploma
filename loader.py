from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config_data import config
from states.mystates import MyStates


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
base_request = config.request_params
cache = {}

