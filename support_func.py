import json
from configs.log_config import *


def text_from_json(*name: str, json_name="texts.json") -> str:
    try:
        logging.info(f"Returning text {name} from json - started")
        with open(file=json_name, mode="r", encoding="UTF-8") as file:
            js_file = json.load(file)
        logging.info(f"Returning text {name} from json - finished successfully")
        if name.__len__() == 1:
            return js_file[name[0]]
        return js_file[name[0]][name[1]]
    except Exception as error:
        logging.error(f"Returning text from json failed: {error}")

