import json
from configs.log_config import *


def text_from_json(*name: str, json_name="texts.json") -> str:
    """
    Функция возвращает значения файла-json по поля

    :param name: Название поля
    :param json_name: Путь до файла-json
    :return: Строка содержимым файла-json по полю "name"
    """
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


def phone_formatter(phone: str, output=False) -> str:
    """
    Функция возвращает отформатированный номер телефона. Например:
        - На входе phone = "   8(9 99)-55566 77 "
        - При output = False -> "89995556677"
        - При output = True  -> "+7 (999) 555-66-77"

    :param phone: Номер телефона
    :param output: Формат вывода
    :return: Отформатированный номер телефона
    """
    pattern = ["-", "+", " ", "(", ")"]
    for pat in pattern:
        phone = phone.replace(pat, "")
    if output:
        phone = f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    return phone


def date_formatter(date: str) -> str:
    """
    Функция возвращает отформатированную строку даты.

    Например: "2001-01-01 00:00:00" -> "01.01.2001"

    :param date: Строка с датой
    :return: Форматированная дата
    """
    return ".".join(date[:10].split("-")[::-1])
