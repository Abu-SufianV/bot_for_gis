import telebot
import support_func as sup
from db.db_manipulation import Database
from configs.patterns import *
from configs.log_config import *
from configs.bot_token import TOKEN

# Запускаем бота
logging.info(f"Connecting to Bot")
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

# Подключаемся к БД
logging.info(f"Connecting to Database")
db = Database()

bot.polling(none_stop=True, interval=0)
# db.query_to_db("DROP TABLE user")
# db.create_all_tables()
