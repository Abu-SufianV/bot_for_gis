import telebot
import support_func as sup
from datetime import datetime
from db.db_manipulation import Database
from configs.patterns import *
from configs.log_config import *
from configs.bot_token import TOKEN

logging.info(f"- - - - Start program - - - -")

# Запускаем бота
try:
    logging.info(f"Connecting to Bot")
    bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
except Exception as error:
    logging.error(f"Error connecting to Bot: {error}")
    raise error

# Подключаемся к БД
try:
    logging.info(f"Connecting to Database")
    db = Database()
except Exception as error:
    logging.error(f"Error connecting to Database: {error}")
    raise error


def user_in_system(id_user: int) -> None:
    """
    Функция вывода информации о пользователе

    :param id_user: ID пользователя
    """
    user_data = db.user_all_info(id_user)
    status = user_data[0][10]
    text_message = ""
    if status == "done":
        text_message = get_user_all_info(id_user)
        bot.send_message(id_user, text_message)
    else:
        text_message = "Вы не окончили регистрацию\nЧтобы продолжить регистрацию, введите \"Ок\""
        bot.send_message(id_user, text_message)

    if text_message:
        logging.info(f"Message send to user: {text_message}")


def get_user_all_info(id_user: int) -> str:
    """
    Функция возвращает всю информацию о пользователя

    :param id_user: ID пользователя
    :return: строка со всей информацией о пользователе
    """
    user_data = db.user_all_info(id_user)
    if user_data[3] == None:
        full_name = f"{user_data[2]} {user_data[1]}"
    else:
        full_name =f"{user_data[2]} {user_data[1]} {user_data[3]}"
    text_message = sup.text_from_json("old_user").format(
        full_name,
        sup.date_formatter(user_data[4]),
        user_data[5],
        user_data[6],
        user_data[7],
        user_data[8]
    )

    return text_message


def get_replay_markup(command: str) -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    all_dept = db.select_to_db("SELECT name FROM departments")
    all_targ = db.select_to_db("SELECT name FROM targets")
    if command == "done":
        btn1 = telebot.types.KeyboardButton("🪪 Инфо. обо мне")
        btn2 = telebot.types.KeyboardButton("ℹ️ Инфо. о департаметах")
        btn3 = telebot.types.KeyboardButton("📃 Подать заявку")
        markup.add(btn1, btn2, btn3)
        return markup
    elif command == "📃 Подать заявку":
        for row in all_dept:
            btn = telebot.types.KeyboardButton(row[0])
            markup.add(btn)
        return markup
    elif (command,) in all_dept:
        res = db.select_to_db(
            f"SELECT t1.name FROM targets t1 JOIN departments t2 "
            f"on t1.id_department = t2.id_department WHERE t2.name = \"{command}\"")
        for row in res:
            btn = telebot.types.KeyboardButton(row[0])
            markup.add(btn)
        return markup
    elif (command,) in all_targ:
        btn1 = telebot.types.KeyboardButton("❌ Отменить заявку")
        btn2 = telebot.types.KeyboardButton("✅ Всё верно")
        markup.add(btn1, btn2)
        return markup


def gen_markup_for_sing_up() -> telebot.types.InlineKeyboardMarkup:
    """
    Функция генерирует кнопку для регистрации

    :return: Кнопку для регистрации
    """
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(telebot.types.InlineKeyboardButton("Зарегистрироваться", callback_data="sing_up"))
    return markup


def gen_markup_for_depart() -> telebot.types.InlineKeyboardMarkup:
    """
    Функция генерирует кнопки для вывода инфомарции о департаметах

    :return: Кнопки с названиями департаметов
    """
    all_dept = db.select_to_db("SELECT name FROM departments")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    for row in all_dept:
        markup.add(telebot.types.InlineKeyboardButton(row[0],
                                                      callback_data=row[0]))
    return markup


def user_sing_up(id_user: int) -> None:
    bot.send_message(chat_id=id_user,
                     text=sup.text_from_json("new_user"),
                     reply_markup=gen_markup_for_sing_up())


@bot.message_handler(commands=["start"])
def start_message(message) -> None:
    """
    Обработка команды /start

    :param message: Данные от пользователя
    """
    id_user = message.from_user.id
    logging.info(f"User {id_user} use command \"/start\"")

    bot.send_message(chat_id=id_user,
                     text=sup.text_from_json("start").format(message.from_user.first_name))

    if db.user_in_system(id_user=id_user):
        user_in_system(id_user=id_user)
    else:
        user_sing_up(id_user=id_user)


@bot.message_handler(commands=["help"])
def start_message(message) -> None:
    """
    Обработка команды /help

    :param message: Данные от пользователя
    """

    bot.send_message(chat_id=message.from_user.id,
                     text=sup.text_from_json("help").format(message.from_user.first_name),
                     )


@bot.message_handler(content_types=["text"])
def main_message(message) -> None:
    id_user = message.from_user.id
    logging.info(f"Message from #{id_user}: {message.text}")
    if message.text == "SOS!":
        # Пользователь ввёл сообщение "SOS!"
        bot.send_message(chat_id=196038837,
                         text=sup.text_from_json("sos").format(message.from_user.username))
        bot.send_message(chat_id=message.chat.id,
                         text='*Сигнал бедствия принят!*\nСвяжемся с Вами в ближайшее время')
    if not db.user_in_system(id_user):
        user_sing_up(id_user)
        return
    status = db.get_sing_up_status(id_user)

    if status == "done":
        # Пользователь зарегистрирован в системе
        all_dept = db.select_to_db("SELECT name FROM departments")
        all_targ = db.select_to_db("SELECT name FROM targets")
        if message.text == "🪪 Инфо. обо мне":
            bot.send_message(chat_id=message.chat.id,
                             text=get_user_all_info(id_user))
        elif message.text == "📃 Подать заявку":
            bot.send_message(chat_id=message.chat.id,
                             text="Выберите отделение",
                             reply_markup=get_replay_markup(message.text))
        elif message.text == "ℹ️ Инфо. о департаметах":
            bot.send_message(chat_id=message.chat.id,
                             text="Выберите отделение",
                             reply_markup=gen_markup_for_depart())
        elif (message.text,) in all_dept:
            id_department = \
                db.select_to_db(f"SELECT id_department FROM departments WHERE name = \"{message.text}\"")[0][
                    0]
            db.new_application([id_user, id_department])
            bot.send_message(chat_id=message.chat.id,
                             text="Выберите услугу",
                             reply_markup=get_replay_markup(message.text))
        elif (message.text,) in all_targ:
            id_target = db.select_to_db(f"SELECT * FROM targets WHERE name = \"{message.text}\"")[0][0]
            db.query_to_db(f"UPDATE applications SET id_target = {id_target} "
                           f"WHERE id_user = {id_user} "
                           f"AND id_application IN (SELECT max(id_application)"
                           f"FROM applications WHERE id_user = {id_user})")

            user_data = list(db.get_all_apls_data(id_user=id_user))
            if user_data[2] is None:
                full_name = " ".join(user_data[:2])
            else:
                full_name = " ".join(user_data[:3])
            user_data = [x for i, x in enumerate(user_data) if i not in [0, 1, 2]]
            user_data.insert(0, full_name)
            user_data[1] = sup.date_formatter(user_data[1])
            send_text = sup.text_from_json("application_confirm").format(*user_data)
            bot.send_message(chat_id=message.chat.id,
                             text=send_text,
                             reply_markup=get_replay_markup(message.text))
        elif message.text == "❌ Отменить заявку":
            db.query_to_db(f"DELETE FROM applications "
                           f"WHERE id_user = {id_user} "
                           f"AND id_application IN (SELECT max(id_application)"
                           f"FROM applications WHERE id_user = {id_user})")

            bot.send_message(chat_id=message.chat.id,
                             text='Заявка была отменена',
                             reply_markup=get_replay_markup("done"))
        elif message.text == "✅ Всё верно":
            bot.send_message(chat_id=message.chat.id,
                             text=sup.text_from_json("application_add"),
                             reply_markup=get_replay_markup("done"))
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Чем можем Вам помочь?",
                             reply_markup=get_replay_markup(status))
    elif status == "start":
        # Начал процесс регистрации

        try:
            full_name = str(message.text).strip()

            for letter in full_name:
                if letter in special_symbols:
                    raise bot.send_message(chat_id=id_user,
                                           text=sup.text_from_json("error", "name"))

            full_name = full_name.split()
            if full_name.__len__() not in [2, 3]:
                raise sup.text_from_json("error", "name")

            for name in full_name:
                if name.__len__() <= 2:
                    raise sup.text_from_json("error", "name")

            db.update_user(id_user=id_user,
                           column_name="name",
                           data=full_name[1].capitalize())

            db.update_user(id_user=id_user,
                           column_name="surname",
                           data=full_name[0].capitalize())

            if full_name.__len__() == 3:
                db.update_user(id_user=id_user,
                               column_name="middle_name",
                               data=full_name[2].capitalize())

            db.set_sing_up_status(id_user=id_user, new_status="full_name")

            bot.send_message(chat_id=id_user, text=sup.text_from_json("birth_date"))
        except Exception as error:
            bot.send_message(chat_id=id_user, text=sup.text_from_json("error", "name"))

    elif status == "full_name":
        # Пользователь ввёл ФИО, теперь дата рождения
        try:
            birth_date = datetime.strptime(message.text, "%d.%m.%Y")
            db.update_user(id_user=id_user,
                           column_name="birth_date",
                           data=birth_date)

            db.set_sing_up_status(id_user=id_user,
                                  new_status="passport")

            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("passport"))

        except Exception as error:
            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("error", "birth_date"))
    elif status == "passport":
        # Пользователь ввёл дату рождения, теперь паспорт
        passport = str(message.text)
        if passport.isdigit() and passport.__len__() == 10:
            passport = f"{passport[:4]} {passport[4:]}"
            db.update_user(id_user=id_user,
                           column_name="passport",
                           data=passport)

            db.set_sing_up_status(id_user=id_user,
                                  new_status="snils")

            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("snils"))
        else:
            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("error", "passport"))
    elif status == "snils":
        # Пользователь ввёл паспорт, теперь СНИЛС
        snils = str(message.text).replace("-", "").strip()
        if snils.isdigit() and snils.__len__() == 11:
            snils = f"{snils[:3]}-{snils[3:6]}-{snils[6:9]}-{snils[9:]}"
            db.update_user(id_user=id_user,
                           column_name="snils",
                           data=snils)

            db.set_sing_up_status(id_user=id_user,
                                  new_status="phone_number")

            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("phone_number"))
        else:
            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("error", "snils"))
    elif status == "phone_number":
        # Пользователь ввёл СНИЛС, теперь номер телефона
        phone = sup.phone_formatter(phone=message.text)

        if phone.isdigit() and phone.__len__() == 11:
            phone = sup.phone_formatter(phone=phone,
                                        output=True)

            db.update_user(id_user=id_user,
                           column_name="phone_number",
                           data=phone)

            db.set_sing_up_status(id_user=id_user,
                                  new_status="email_address")

            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("email_address"))
        else:
            bot.send_message(chat_id=id_user,
                             text=sup.text_from_json("error", "phone_number"))
    elif status == "email_address":
        # Пользователь ввёл номер телефона, теперь e-mail
        email = str(message.text).strip()

        if "@" in email and "." in email:
            email_dog = email.split("@")[0]
            email_dot = email.split("@")[1].split(".")
            if email_dog.__len__() > 0 and email_dot[0].__len__() > 0 and email_dot[1].__len__() > 0:
                db.update_user(id_user=id_user,
                               column_name="email_address",
                               data=email)

                db.set_sing_up_status(id_user=id_user,
                                      new_status="done")

                bot.send_message(chat_id=id_user,
                                 text=sup.text_from_json("done"))

                bot.send_message(chat_id=message.chat.id,
                                 text="Чем можем Вам помочь?",
                                 reply_markup=get_replay_markup("done"))
            else:
                bot.send_message(id_user, text=sup.text_from_json("error", "email_address"))
        else:
            bot.send_message(id_user, text=sup.text_from_json("error", "email_address"))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    all_dept = db.select_to_db("SELECT name FROM departments")

    if call.data == "sing_up":
        db.new_user(id_user=call.from_user.id)
        bot.send_message(chat_id=call.from_user.id,
                         text="Введите ФИО через пробел.\nНапример: Иванов Иван Иванович")
    if (call.data,) in all_dept:
        dep_info = db.select_to_db(f"SELECT name, location, work_from, work_to "
                                   f"FROM departments where name=\"{call.data}\"")[0]
        send_text = sup.text_from_json("department").format(*dep_info)
        bot.send_message(chat_id=call.from_user.id,
                         text=send_text,
                         reply_markup=get_replay_markup("done"))


bot.polling(none_stop=True, interval=0)
