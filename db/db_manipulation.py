import sqlite3 as sql
from configs.log_config import *
from configs.db_config import DB_PATH


class Database:
    """
    Класс позволяет производить взаимодействие Telegram-Bot c БД

    Возможности класса:
        - создание таблиц;
        - добавление, изменение, удаление строк из таблиц;
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_table_user(self) -> None:
        """
        Создание таблицы USERS
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'USERS' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users(
                        id_user INTEGER PRIMARY KEY,
                        name VARCHAR(255),
                        surname VARCHAR(255),
                        middle_name VARCHAR(255),
                        birth_date TIMESTAMP,
                        passport VARCHAR(10),
                        snils VARCHAR(9),
                        phone_number VARCHAR(20),
                        email_address VARCHAR(200),
                        sing_up_date TIMESTAMP NOT NULL,
                        sing_up_status VARCHAR(15)
                    )
                    """
                )

                logging.info("Table 'USERS' create - finished successfully!")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_apls(self) -> None:
        """
        Создание таблицы APPLICATIONS
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'APPLICATIONS' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS applications(
                        id_application INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_user INTEGER NOT NULL,
                        id_department INTEGER NOT NULL,
                        id_target INTEGER,                
                        date_stamp TIMESTAMP NOT NULL
                    )
                    """
                )

                logging.info("Table 'APPLICATIONS' create - finished successfully")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_targ(self) -> None:
        """
        Создание таблицы TARGETS
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'TARGETS' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS targets(
                        id_target INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_department INTEGER NOT NULL,
                        name VARCHAR(255) NOT NULL
                    )
                    """
                )

                logging.info("Table 'TARGETS' create - finished successfully")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_dept(self) -> None:
        """
        Создание таблицы DEPARTMENTS
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'DEPARTMENTS' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS departments (
                        id_department INTEGER PRIMARY KEY AUTOINCREMENT,
                        name INTEGER NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        work_from VARCHAR(5) NOT NULL,
                        work_to VARCHAR(5) NOT NULL
                    )
                    """
                )

                logging.info("Table 'DEPARTMENTS' create - finished successfully")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def list_all_tables(self) -> list[str]:
        """
        Вывод всех кастомных таблиц из БД

        :return: Список названий таблиц БД
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Select all custom tables from DB - started")

                result = cursor.execute(f"""
                                        SELECT name 
                                        FROM sqlite_master 
                                        WHERE 1 = 1
                                        AND type='table' 
                                        AND LOWER(name) not like '%sql%';
                                        """).fetchall()

                logging.info("Select all custom tables from DB - finished successfully")
            return result
        except Exception as error:
            logging.error(f"Query failed: {error}")

    def create_all_tables(self) -> None:
        """
        Создание всех таблиц

        :return:
        """
        self.create_table_user()
        self.create_table_apls()
        self.create_table_dept()
        self.create_table_targ()

    def delete_all_table(self) -> None:
        """
        Удаление всех таблиц из БД
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()
                logging.info("Delete all tables from DB started")
                tables_list = self.list_all_tables()

                # return list(tables_list[0])[0]

                for table in tables_list:
                    table = list(table)[0]
                    logging.debug(f"DROP TABLE IF EXISTS {table};")
                    cursor.execute(f"DROP TABLE IF EXISTS {table};")

                logging.info("Delete all tables from DB - finished successfully")
        except Exception as error:
            logging.error(f"Delete tables failed: {error}")

    def select_to_db(self, query: str) -> list[tuple]:
        """
        Запрос в БД с дальнейшим возвратом результата выборки

        :param query: текст запроса
        :return: результат запроса выборки
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Select query - started: {query}")

                result = cursor.execute(query).fetchall()
                result_count = len(result)

                if result_count > 1:
                    logging.info(f"Select query return {result_count} rows")
                else:
                    logging.info(f"Select query return {result_count} row")

                return result
        except Exception as error:
            logging.error(f"Select query failed: {error}")

    def update_user(self, id_user: int, column_name: str, data: str) -> None:
        """
        Изменение строки в таблице USERS по полю id_user

        :param id_user: ID пользователя
        :param column_name: изменяемое поле
        :param data: данные вносимые в поле
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Insert into table 'USERS' in {column_name} data: {data} ")
                logging.debug(f"Query: INSERT INTO users('{column_name}') VALUES ('{data}'); ")

                cursor.execute(f"""
                                UPDATE users
                                SET 
                                {column_name} = '{data}'
                                WHERE id_user = {id_user}
                                ; """)

                logging.info(f"Insert - finished successfully")
        except Exception as error:
            logging.error(f"Insert query failed: {error}")

    def new_application(self, data: list) -> None:
        """
        Добавляет запись в таблицу APPLICATIONS

        :param data: id_user и id_department
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Insert into table 'APPLICATIONS' data {data} ")

                cursor.execute(f"""INSERT INTO applications (id_application, id_user, id_department, date_stamp) 
                                    VALUES (NULL,?,?,'{datetime.now()}'); """, data)

                logging.info(f"Insert - finished successfully")
        except Exception as error:
            logging.error(f"Insert query failed: {error}")

    def query_to_db(self, query: str) -> None:
        """
        Запрос в БД не возвращающий данных

        :param query: текст запроса
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Query - started: {query}")

                cursor.execute(query)

                logging.info("Query - finished successfully")
        except Exception as error:
            logging.error(f"Query failed: {error}")

    def user_in_system(self, id_user: int) -> bool:
        """
        Проверка на наличие пользователя в БД

        :param id_user: ID пользователя
        :return: возвращает True, если пользователь найден
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Search user #{id_user} in DB")

                result = cursor.execute(f"""
                                SELECT name, surname 
                                FROM users
                                WHERE id_user = {id_user}
                                """).fetchall()
                if result.__len__() == 0:
                    logging.info(f"User #{id_user} - False")
                    return False
                logging.info(f"User #{id_user} - True")
                return True
        except Exception as error:
            logging.error(f"Query failed: {error}")

    def user_all_info(self, id_user: int) -> tuple:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Get all info for user #{id_user}")

                result = cursor.execute(f"""
                                SELECT * FROM users 
                                WHERE id_user = {id_user}
                                """).fetchall()[0]

                logging.info(f"Info ready for #{id_user}: {result}")

                return result
        except Exception as error:
            logging.error(f"Get all info #{id_user} failed: {error}")

    def new_user(self, id_user: int) -> None:
        """
        Добавление нового пользователя в таблицу USERS

        :param id_user: ID пользователя
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Creating new user: {id_user}")

                cursor.execute(f"""
                                INSERT INTO users(id_user, sing_up_date, sing_up_status) 
                                VALUES ('{id_user}','{datetime.now()}','start'); """)

                logging.info(f"Sing up status for #{id_user}")
        except Exception as error:
            logging.error(f"Get status #{id_user} failed: {error}")

    def get_sing_up_status(self, id_user: int) -> str:
        """
        Определяет статус регистрации пользователя

        :param id_user: birth_date пользователя
        :return: статус пользователя
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Get status user #{id_user} for sing up")

                result = cursor.execute(f"""
                                SELECT sing_up_status 
                                FROM users
                                WHERE id_user = {id_user}
                                """).fetchone()

                logging.info(f"Sing up status for #{id_user} - {result[0]}")
                return result[0]
        except Exception as error:
            logging.error(f"Get status #{id_user} failed: {error}")

    def set_sing_up_status(self, id_user: int, new_status: str) -> None:
        """
        Изменение текущего статуса пользователя

        :param id_user: ID пользователя
        :param new_status: новый статус
        """
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Set status user #{id_user} to '{new_status.upper()}'")

                cursor.execute(f"""
                                UPDATE users
                                SET sing_up_status = '{new_status}'
                                WHERE id_user = {id_user}
                                """)

                logging.info(f"Set status user #{id_user} - finished successfully")
        except Exception as error:
            logging.error(f"Set status failed: {error}")

    def get_all_apls_data(self, id_user: int) -> list:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Get all data about application to #{id_user}")

                res = cursor.execute(f"""
                    SELECT DISTINCT 
                    us.surname,
                    us.name,
                    us.middle_name, 
                    us.birth_date,
                    us.passport, 
                    us.snils, 
                    us.phone_number, 
                    us.email_address,
                    dep.name,
                    tar.name,
                    dep.location,
                    dep.work_from,
                    dep.work_to 
                    FROM users as us 
                    JOIN applications as app ON app.id_user = us.id_user 
                    JOIN departments as dep ON dep.id_department = app.id_department 
                    JOIN targets as tar ON tar.id_target = app.id_target
                    WHERE us.id_user = {id_user} 
                    AND app.id_application IN (SELECT max(id_application) 
                    FROM applications WHERE id_user = {id_user})
                """).fetchall()[0]

                logging.info(f"Get all data about application to #{id_user} - finished successfully")
                return res
        except Exception as error:
            logging.error(f"Get all data: {error}")
