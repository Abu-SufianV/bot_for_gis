import sqlite3 as sql
from configs.log_config import *
from configs.db_config import DB_PATH


class Database:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_table_person(self) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS person(
                        id_person INTEGER PRIMARY KEY AUTOINCREMENT,
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

                logging.info("Table PERSON created successfully!")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_table_applications(self) -> None:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS applications(
                        id_application INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_person INTEGER NOT NULL,
                        type_application VARCHAR(255) NOT NULL,
                        departament VARCHAR(255) NOT NULL,
                        target VARCHAR(255) NOT NULL,                
                        timestamp INTEGER NOT NULL,
                        date_app INTEGER,
                        result BLOB,
                        cancel_reason VARCHAR(255) NOT NULL
                    )
                    """
                )

                logging.info("Table APPLICATIONS created successfully!")
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")

    def create_all_tables(self) -> None:
        self.create_table_person()
        self.create_table_applications()

    def select_to_db(self, query: str) -> None | list:
        try:
            with sql.connect(self.db_path) as db:
                cursor = db.cursor()
                result = cursor.execute(query).fetchall()
                result_count = len(result)

                logging.info(f"Select query: {query}")

                if result_count > 1:
                    logging.info(f"Select query return {result_count} rows")
                else:
                    logging.info(f"Select query return {result_count} row")

                return result
        except Exception as error:
            logging.error(f"Query to DB finished with errors: {error}")
