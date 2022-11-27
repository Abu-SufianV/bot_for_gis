import sqlite3 as sql
from configs.log_config import *
from configs.db_config import DB_PATH


class Database:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_table_user(self) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'USER' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user(
                        id_user INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        surname VARCHAR(255) NOT NULL,
                        middle_name VARCHAR(255),
                        birth_date INTEGER NOT NULL,
                        snils VARCHAR(9),
                        passport VARCHAR(10),
                        phone_number VARCHAR(20),
                        email_address VARCHAR(200)
                    )
                    """
                )

                logging.info("Table 'USER' create - finished successfully!")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_apls(self) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info("Table 'APPLICATIONS' create - started")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS applications(
                        id_application INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_user INTEGER NOT NULL,
                        type_application VARCHAR(255) NOT NULL,
                        id_department INTEGER NOT NULL,
                        target VARCHAR(255) NOT NULL,                
                        date_stamp TIMESTAMP NOT NULL,
                        date_app TIMESTAMP,
                        result BLOB,
                        cancel_reason VARCHAR(255) NOT NULL
                    )
                    """
                )

                logging.info("Table 'APPLICATIONS' create - finished successfully")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_dept(self) -> None:
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
        self.create_table_user()
        self.create_table_apls()
        self.create_table_dept()

    def delete_all_table(self):
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

    def select_to_db(self, query: str) -> list:
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

    def insert_into_user(self, data: list) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Insert into table 'USER' data {data} ")

                cursor.execute(f"""INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?); """, data)

                logging.info(f"Insert - finished successfully")
        except Exception as error:
            logging.error(f"Insert query failed: {error}")

    def insert_into_app(self, data: list) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Insert into table 'APPLICATIONS' data {data} ")

                cursor.execute(f"""INSERT INTO applications VALUES (NULL,?,?,?,?,?,?,?,?); """, data)

                logging.info(f"Insert - finished successfully")
        except Exception as error:
            logging.error(f"Insert query failed: {error}")

    def query_to_db(self, query: str) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Query - started: {query}")

                cursor.execute(query)

                logging.info("Query - finished successfully")
        except Exception as error:
            logging.error(f"Query failed: {error}")

    def user_in_system(self, id_user: int) -> bool:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()

                logging.info(f"Search user #{id_user} in DB")

                result = cursor.execute(f"""
                                SELECT name, surname 
                                FROM user
                                WHERE id_user = {id_user}
                                """).fetchall()
                if result.__len__() == 0:
                    logging.info(f"User #{id_user} - False")
                    return False
                logging.info(f"User #{id_user} - True")
                return True
        except Exception as error:
            logging.error(f"Query failed: {error}")
