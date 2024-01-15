import pandas as pd
import psycopg2

import config
import clean_insert_data as cid


CONFIG = config.get_db_config()
IMAGE_FOLDER_PATH = config.get_img_path()



def postgres_execute_insert_query(query: str) -> None:
    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        # print(query)
        print("Insertion Done")

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")


def postgres_execute_search_query(table: str, column: str, ref: str) -> None:
    """test de connection sur la db"""

    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()

        query = f"""
                SELECT {column} FROM {table}
                WHERE {ref} ==
                """
        cursor.execute(query)
        resultat = cursor.fetchone()
        print(f"{resultat}")
        print("Insertion Done")

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")


def insert_view_ref(df: pd.DataFrame) -> None:
    ## - insert view
    view_name = df['view_desc'].unique()

    for view in view_name:
        query = f"""
                INSERT INTO view_ref (view_name)
                VALUES ('{view}')
                ON CONFLICT (view_name)
                DO NOTHING;
                """
        postgres_execute_insert_query(query)


def insert_collection_ref(df: pd.DataFrame) -> None:
    ## - insert collection in collection_ref table
    collection_name = df['collection'].unique()

    for collection in collection_name:
        query = f"""
                INSERT INTO collection_ref (collection_name)
                VALUES ('{collection}')
                ON CONFLICT (collection_name)
                DO NOTHING;
                """
        postgres_execute_insert_query(query)


def insert_tablet_ref(df: pd.DataFrame) -> None:
    tablet_name = df['tablet_CDLI'].unique()

    for tablet in tablet_name:
        ## - Get the corresponding image
        img_encode = cid.get_image(tablet, IMAGE_FOLDER_PATH)
        id_collection = postgres_execute_search_query('collection_ref',
                                                      'id_collection',
                                                      'collection_name')


        query = f"""
                INSERT INTO tablet_ref (tablet_name, picture, id_collection)
                VALUES ({tablet}, {img_encode}, {id_collection})
                ON CONFLICT ({tablet})
                DO NOTHING;
                """
        postgres_execute_insert_query(query)






