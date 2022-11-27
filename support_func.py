import json
from configs.log_config import *


def text_from_json(name: str, json_name="texts.json") -> str:
    try:
        logging.info("Returning text from json - started")
        with open(file=json_name, mode="r", encoding="UTF-8") as file:
            js_file = json.load(file)
        logging.info("Returning text from json - finished successfully")
        return js_file[name]
    except Exception as error:
        logging.error(f"Returning text from json failed: {error}")

