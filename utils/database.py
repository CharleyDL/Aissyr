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
    """Check user account based on email, and retrieves it from the database.
    If the account exists, it returns a dictionary containing the account 
    information. If no account is found with the given email, it returns None.

    Args:
        email (str): The email address of the user to verify.

    Returns:
        dict or None: A dictionary containing the user account information 
        if the account exists ; None if no account is found with the given email.
    """
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           SELECT *
                           FROM account_user
                           WHERE email=%s;
                           """, (email,))

        data = db.cursor.fetchone()
        if data is None:
            return None

    return {
        "id_account": data[0],
        "title": data[1],
        "last_name": data[2],
        "first_name": data[3],
        "email": data[4],
        "pwd_hash": data[5]
    }


def create_account(payload: dict) -> bool:
    """
    Create a new user account in the database with the provided payload
    containing account information. 
    If an account already exists, the function will not create a new account 
    and will return False. Otherwise, it will insert the new account and 
    return True.

    Args:
        payload (dict): A dictionary containing the account information 
        including 'title', 'last_name', 'first_name', 'email', and 'pwd_hash'.

    Returns:
        bool: True if the account was successfully created, False otherwise.
    """

    with PgDatabase() as db:
        db.cursor.execute(f"""
            INSERT INTO account_user (title, last_name, 
                                      first_name, email, pwd_hash)
            SELECT %s, %s, %s, %s, %s
            WHERE NOT EXISTS (SELECT 1 FROM account_user WHERE email = %s)
            """, (payload.title, 
                  payload.last_name, 
                  payload.first_name, 
                  payload.email,
                  payload.pwd_hash,
                  payload.email))

        if db.cursor.rowcount > 0:
            db.connection.commit()
            return True
        else:
            db.connection.rollback()
            return False


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
