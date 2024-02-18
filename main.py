from loader import bot
import keyboards
import handlers
from utils.set_bot_commands import set_default_commands
from database.db_init import init_db

if __name__ == "__main__":
    init_db()
    set_default_commands(bot)
    bot.infinity_polling()
