import pandas as pd
import psycopg2

import config
import clean_insert_data as cid


CONFIG = config.get_db_config()
CSV_FOLDER_PATH = config.get_csv_path()
IMAGE_FOLDER_PATH = config.get_img_path()
CSV_FILES = cid.get_files_path(CSV_FOLDER_PATH)



def postgres_execute_insert_query(query: str) -> None:
    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()

        print("Insertion Done")

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")


def postgres_execute_search_query(table: str, target_col: str, 
                                  ref_col: str, ref_value: str) -> tuple:
    """
    Execute a search query in a PostgreSQL database.

    Parameters:
    -----------
    - table_name (str, required): Table name to search in.
    - target_col (str, required): Column from which to retrieve data.
    - ref_col (str, required): Column to use as a reference for the search.
    - ref_value (str, required): Value to search in the reference column.

    Returns:
    --------
    None
    """
    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()

        query = f"""
                SELECT {target_col} FROM {table}
                WHERE {ref_col} = '{ref_value}';
                """
        cursor.execute(query)
        result = cursor.fetchone()

        # print(f"{result}")

        return result

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            # print("PostgreSQL connection is closed")


def insert_view_ref(df: pd.DataFrame) -> None:
    view_name = sorted(df['view_desc'].unique())
    # print(view_name)

    for view in view_name:
        query = f"""
                INSERT INTO view_ref (view_name)
                VALUES ('{view}')
                ON CONFLICT (view_name)
                DO NOTHING;
                """
        postgres_execute_insert_query(query)


def insert_collection_ref(df: pd.DataFrame) -> None:
    collection_name = sorted(df['collection'].dropna().unique())
    # print(collection_name)

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
        ## - Get encoding image to insert in BYTEA
        img_encode = cid.get_image(tablet, IMAGE_FOLDER_PATH)

        ## - Retrieve id_collection to insert
        coll_ref = df.loc[df['tablet_CDLI'] == tablet, 'collection'].unique()
        id_collection = postgres_execute_search_query('collection_ref', 'id_collection',
                                                      'collection_name', str(coll_ref[0]))

        query = f"""
                INSERT INTO tablet_ref (tablet_name, picture, id_collection)
                VALUES ('{tablet}', '{img_encode}', {id_collection[0]})
                ON CONFLICT (tablet_name)
                DO NOTHING;
                """

        postgres_execute_insert_query(query)


def insert_segment_ref(df: pd.DataFrame) -> None:
    ## - DF qui est le bbox_annotation_train puis test
    ## - Get segment_idx
    segm_idx = df['segm_idx'].unique()

    for segment in segm_idx:
        ## - Get id_collection, id_tablet and id_view from DB
        collection_ref = df.loc[df['segm_idx'] == segment, 'collection'].unique()
        id_collection = postgres_execute_search_query('collection_ref', 'id_collection', 
                                                'collection_name', str(collection_ref[0]))

        tablet_ref = df.loc[df['segm_idx'] == segment, 'tablet_CDLI'].unique()
        id_tablet = postgres_execute_search_query('tablet_ref', 'id_tablet', 
                                                'tablet_name', str(tablet_ref[0]))

        view_ref = df.loc[df['segm_idx'] == segment, 'view_desc'].unique()
        id_view = postgres_execute_search_query('view_ref', 'id_view', 
                                                'view_name', str(view_ref[0]))


        print(segment, id_collection[0], id_tablet[0], id_view[0])

        ## - Get all information from df
        # bbox = df.loc[df['segm_idx'] == segment, 'bbox'].unique()
        # scale = df.loc[df['segm_idx'] == segment, 'scale'].unique()



        # print(segment, bbox[0], scale[0], id_view[0], id_tablet[0])

        # query = f"""
        #         INSERT INTO segment_ref (segment_idx, bbox_segment, scale,
        #                                  id_view, id_tablet)
        #         VALUES ('{segment}', '{bbox[0]}', {scale[0]}, 
        #                  {id_view[0]}, {id_tablet[0]})
        #         ON CONFLICT (segment_idx)
        #         DO NOTHING;
        #         """


#   segment_idx
#   bbox_segment 
#   scale  
#   id_view
#   id_tablet