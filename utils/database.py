import os
import psycopg2 as pg

import utils.functions as fct

from abc import ABC, abstractmethod
from datetime import date




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
    -----
        email (str): The email address of the user to verify.

    Returns:
    -------
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
    -----
        payload (dict): A dictionary containing the account information 
        including 'title', 'last_name', 'first_name', 'email', and 'pwd_hash'.

    Returns:
    -------
        bool: True if the account was successfully created, False otherwise.
    """

    ## - Hash the password before storing it in the database
    hash_password = fct.hash_bcrypt(payload.password)

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
                  hash_password,
                  payload.email))

        if db.cursor.rowcount > 0:
            db.connection.commit()
            return True
        else:
            db.connection.rollback()
            return False


## ------------------------------- ANNOTATION ------------------------------- ##

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


## ------------------------------- RESOURCES -------------------------------- ##

def select_all_glyphs() -> dict:
    """
    Retrieves all glyphs from the database with their information.

    Returns:
    -------
        dict: A dictionary containing glyph information. 
        The keys are integers representing the index of the glyph, and the values 
        are dictionaries containing the glyph details, including 
        'mzl_number', 'glyph_name', 'glyph', and 'glyph_phonetic'.
    """
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           SELECT mzl_number, glyph_name, glyph, glyph_phonetic
                           FROM mzl_ref;
                           """)
        data = db.cursor.fetchall()
        if data is None:
            return None
 
    glyph_info = {}
    for i, row in enumerate(data, start=1):
        mzl_number, glyph_name, glyph, glyph_phonetic = row
        phonetic_list = None
        if glyph_phonetic is not None:
            phonetic_list = glyph_phonetic[1:-1].split(",")
            phonetic_list = [phoneme.strip() for phoneme in phonetic_list]

        glyph_info[i] = {
            "mzl_number": mzl_number,
            "glyph_name": glyph_name,
            "glyph": glyph,
            "glyph_phonetic": phonetic_list
        }

    return glyph_info


def select_glyph_by_mzl(mzl_number: int) -> dict:
    """
    Retrieves glyph information from the database based on the given MZL number.

    Args:
    -----
        mzl_number (int): The MZL number to search for in the database.

    Returns:
    ----
        dict: A dictionary containing glyph information, including 'mzl_number',
              'glyph_name', 'glyph', and 'glyph_phonetic'. If no data is found
              for the given MZL number, None is returned.

    Note:
    -----
        If 'glyph_phonetic' is NULL in the database, the corresponding value
        in the returned dictionary will be None.
    """
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           SELECT mzl_number, glyph_name, glyph, glyph_phonetic
                           FROM mzl_ref
                           WHERE mzl_number=%s;
                           """, (mzl_number,))
        data = db.cursor.fetchone()
        if data is None:
            return None

    ## - Extract and joining the phonetic list (in {} otherwise)
    glyph_phonetic = data[3]
    if glyph_phonetic is not None:
        phonetic_list = glyph_phonetic[1:-1].split(",")
        phonetic_list = [phoneme.strip() for phoneme in phonetic_list]
    else:
        phonetic_list = None

    return {
        "mzl_number": data[0],
        "glyph_name": data[1],
        "glyph": data[2],
        "glyph_phonetic": phonetic_list
    }



## ----------------------------- SAVE ANNOTATION ---------------------------- ##

def save_in_tablet_ref(payload: dict) -> int:
    """
    Save tablet reference in the database.

    Args:
    -----
    - payload (dict): A dictionary containing tablet payload.

    Returns:
    - int: The ID of the tablet if successfully saved or already exist.
    """

    with PgDatabase() as db:
        ## - Check if the tablet already exists in the database
        db.cursor.execute("""
                           SELECT id_tablet
                           FROM tablet_ref
                           WHERE tablet_name = %s AND picture = %s;
                           """, (payload.img_name, payload.img))
        existing_tablet = db.cursor.fetchone()

        if existing_tablet:
            return existing_tablet[0]
        else:
            db.cursor.execute("""
                               INSERT INTO tablet_ref (tablet_name,
                                                       set_split, 
                                                       picture,
                                                       id_collection)
                               VALUES (%s, 'annotation', %s, 6)
                               RETURNING id_tablet;
                               """, (payload.img_name, payload.img))

            id_tablet = db.cursor.fetchone()[0]
            db.connection.commit()

            return id_tablet


def save_in_reveal(id_tablet: int) -> None:
    """
    Save reveal information in the database.

    Args:
    -----
    - id_tablet (int): The ID of the tablet.
    """
    with PgDatabase() as db:
        db.cursor.execute("""
                           INSERT INTO reveal (id_tablet, id_view)
                           VALUES (%s, 6)
                           ON CONFLICT (id_tablet, id_view) DO NOTHING;
                           """, (id_tablet,))

        if db.cursor.rowcount > 0:
            db.connection.commit()
        else:
            db.connection.rollback()


def save_in_segment_ref(payload: dict, id_tablet: int) -> int:
    """
    Save segment reference in the database.

    Args:
    -----
    - payload (dict): A dictionary containing segment payload.
    - id_tablet (int): The ID of the tablet.

    Returns:
    - int: The ID of the segment if successfully saved or already exists.
    """
    with PgDatabase() as db:
        ## - Check if the segment already exists in the database
        db.cursor.execute("""
                           SELECT id_segment
                           FROM segment_ref
                           WHERE id_tablet = %s;
                           """, (id_tablet,))
        existing_segment = db.cursor.fetchone()

        if existing_segment:
            return existing_segment[0]
        else:
            db.cursor.execute("""
                               INSERT INTO segment_ref (segment_idx,
                                                        bbox_segment,
                                                        scale,
                                                        id_collection,
                                                        id_tablet,
                                                        id_view)
                               VALUES (999999, %s, NULL, 6, %s, 6)
                               RETURNING id_segment;
                               """, (str(payload.bbox_img), 
                                     id_tablet))

            id_segment = db.cursor.fetchone()[0]

            if id_segment is not None:
                db.connection.commit()
                return id_segment


def save_in_annotation_ref(payload: dict, id_segment: int) -> bool:
    """
    Save annotation reference in the database.

    Args:
    -----
    - payload (dict): A dictionary containing annotation payload.
    - id_segment (int): The ID of the segment.

    Returns:
    -------
    - bool: True if the annotation reference is successfully saved, 
            False otherwise.
    """
    with PgDatabase() as db:
        ## - Check if the annotation already exists in the database
        db.cursor.execute("""
                           SELECT id_annotation
                           FROM annotation_ref
                           WHERE bbox = %s
                           AND relative_bbox = %s
                           AND mzl_number = %s
                           AND id_segment = %s;
                           """, (str(payload.bbox_annotation),
                                 str(payload.bbox_annotation),
                                 payload.mzl_number,
                                 id_segment))
        existing_annotation = db.cursor.fetchone()

        if existing_annotation:
            return False
        else:
            db.cursor.execute("""
                               INSERT INTO annotation_ref (bbox,
                                                           relative_bbox,
                                                           mzl_number,
                                                           id_segment)
                               VALUES (%s, %s, %s, %s);
                               """, (str(payload.bbox_annotation),
                                     str(payload.bbox_annotation),
                                     payload.mzl_number,
                                     id_segment))

            db.connection.commit()
            return True


## --------------------------- SAVE CLASSIFICATION -------------------------- ##

def check_img_name(img_name: str) -> bool|int:
    """
    Check if an image exists in the tablet_infrn table.

    Args:
    -----
        img_name (str): The name of the image to check.

    Returns:
    -------
        boolean or int: Returns False if the tablet name doesn't exist, 
        otherwise returns the id_inference associated with the tablet name.
    """
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           SELECT id_inference
                           FROM tablet_infrn
                           WHERE tablet_name=%s;
                           """, (img_name,))
        data = db.cursor.fetchone()

        if data is None:
            return False

        return data[0]


def save_in_tablet_name(payload: dict, date_infrn: date) -> bool|int:
    """
    Save tablet information into the tablet_infrn table.

    Args:
    ----
    payload: The payload containing tablet information.
    date_infrn (date): The date of the inference.

    Returns:
    -------
    int or bool: Returns the id_inference if the insertion was successful,
    otherwise returns False.
    """
    with PgDatabase() as db:
        db.cursor.execute(f"""
                           INSERT INTO tablet_infrn (tablet_name, 
                                                     picture, 
                                                     date_infrn)
                           VALUES (%s, %s, %s)
                           RETURNING id_inference;
                           """, (payload.img_name, 
                                 payload.img, 
                                 date_infrn))
        id_inference = db.cursor.fetchone()[0]
        db.connection.commit()

        if id_inference is not None:
            db.connection.commit()
            return id_inference
        else:
            db.connection.rollback()
            return False


def save_in_infrn_result(payload: dict, id_inference: int) -> bool:
    """
    Save inference result into the infrn_result table.

    Args:
    ----
        payload: The payload containing inference result information.
        id_inference (int): The id of the inference associated with the result.

    Returns:
    ----
        bool: Returns True if the insertion is successful, 
        otherwise returns False.
    """
    with PgDatabase() as db:
        db.cursor.execute("""
            INSERT INTO infrn_result (bbox, 
                                      confidence,
                                      mzl_number, 
                                      id_inference)
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM infrn_result 
                WHERE bbox = %s 
                AND confidence = %s 
                AND mzl_number = %s 
                AND id_inference = %s
            );
            """, (str(payload.bbox),
                  payload.confidence,
                  payload.mzl_number,
                  id_inference,
                  str(payload.bbox), 
                  payload.confidence, 
                  payload.mzl_number, 
                  id_inference))

        if db.cursor.rowcount > 0:
            db.connection.commit()
            return True
        else:
            db.connection.rollback()
            return False
