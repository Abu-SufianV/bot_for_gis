import logging
from datetime import datetime

log_filename = f"logs/tg_bot__{datetime.date(datetime.now())}.log".replace("-", "_")
log_format = "%(asctime)s [%(levelname)s] %(filename)s - %(funcName)s: %(message)s"
log_level = logging.INFO
log_encoding = "UTF-8"
logging.basicConfig(level=log_level, filename=log_filename, format=log_format, encoding=log_encoding)
