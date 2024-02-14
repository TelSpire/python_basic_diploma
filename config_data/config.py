import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
DEFAULT_COMMANDS = (
    ("hello_world", "Вывести hello world"),
    ("help", "Вывести справку"),
    ("menu", "Показывает доступные кнопки действий"),
    ("history", "Показывает последние 10 запросов")
)
request_params = {
    'origin': '',
    'destination': '',
    'amount': 1,
    'price_min': 0,
    'price_max': 100000,
    'start_date': 1,
    'end_date': 31,
    'min_duration': 1,
    'max_duration': 31
}
