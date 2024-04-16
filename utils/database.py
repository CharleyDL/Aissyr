import os
import psycopg2 as pg

from abc import ABC, abstractmethod # new




class Database(ABC):
    """Database context manager"""

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):
    """PostgreSQL Database context manager"""

    def __init__(self) -> None:
        self.driver = pg
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )



## -------------------------------- ACCOUNT --------------------------------- ##
def verify_user_account(email: str) -> dict:
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           SELECT email, pwd_hash
                           FROM account_user
                           WHERE email=%s;
                           """, (email,))

        data = db.cursor.fetchone()
        if data is None:
            return None

    return {
        "email": data[0],
        "password_hash": data[1]
    }




## ------------------------------ ANNOTATION -------------------------------- ##

def select_annotation() -> list:
    with PgDatabase() as db:
        db.cursor.execute(f"""SELECT *
                              FROM annotation_ref
                              LIMIT 10;
                           """)

        objects = [
            {
                "id_annotation": data[0],
                "bbox": data[1],
                "relative_bbox":data[2],
                "mzl_number":data[3],
                "id_segment": data[4]
            }
            for data in db.cursor.fetchall()
        ]
    return objects