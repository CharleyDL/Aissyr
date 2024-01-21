#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 12 Jan. 2024
# ==============================================================================
# Functions to insert in Postgres DB the data from different csv
# Script defines functions to insert data from different CSV files into
# PostgreSQL tables : view_ref, collection_ref, tablet_ref, and segment_ref 
# tables.
# ==============================================================================

import pandas as pd
import psycopg2

## - Personal librairies
import config
import clean_insert_data as cid

from tqdm import tqdm


CONFIG = config.get_db_config()
CSV_FOLDER_PATH = config.get_csv_path()
IMAGE_FOLDER_PATH = config.get_img_path()
CSV_FILES = cid.get_files_path(CSV_FOLDER_PATH)




def postgres_execute_insert_query(query: str) -> None:
    """
    Execute an INSERT query in a PostgreSQL database.

    Parameter:
    -----------
    query (str, required): The SQL query to be executed.
    """
    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()

        # print("Insertion Done")

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            # print("PostgreSQL connection is closed")


def postgres_execute_search_query(query: str) -> tuple:
    """
    Execute a search query in a PostgreSQL database.

    Parameters:
    -----------
    query (str, required): The SQL query to be executed.

    Return:
    --------
    tuple: Query result
    """
    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()
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
    view_name = df['view_desc'].unique()

    for view in tqdm(view_name):
        query = f"""
                INSERT INTO view_ref (view_name)
                VALUES ('{view}')
                ON CONFLICT (view_name)
                DO NOTHING;
                """
        postgres_execute_insert_query(query)


def insert_collection_ref(df: pd.DataFrame) -> None:
    collection_name = sorted(df['collection'].dropna().unique())

    for collection in tqdm(collection_name):
        query = f"""
                INSERT INTO collection_ref (collection_name)
                VALUES ('{collection}')
                ON CONFLICT (collection_name)
                DO NOTHING;
                """
        postgres_execute_insert_query(query)


def insert_tablet_ref(df: pd.DataFrame, set_split) -> None:
    tablet_name = df['tablet_CDLI'].unique()

    for tablet in tqdm(tablet_name):
        ## - Get encoding image to insert in BYTEA
        img_encode = cid.get_image(tablet, IMAGE_FOLDER_PATH)

        ## - Retrieve id_collection to insert
        coll_ref = df.loc[df['tablet_CDLI'] == tablet, 'collection'].unique()
        search_query = f"""
                        SELECT id_collection FROM collection_ref
                         WHERE collection_name = '{str(coll_ref[0])}';
                        """
        id_collection = postgres_execute_search_query(search_query)

        ## - Insert
        query = f"""
                INSERT INTO tablet_ref (tablet_name, set_split, 
                                        picture, id_collection)
                VALUES ('{tablet}', '{set_split}', 
                        '{img_encode}', {id_collection[0]})
                ON CONFLICT (tablet_name)
                DO NOTHING;
                """

        postgres_execute_insert_query(query)


def insert_segment_ref(df: pd.DataFrame) -> None:
    ## - Get all segm_idx corresponding to a collection, 
    ##   same segm_idx in diff collection  (e.g., 0 in 'train', 0 in 'saa09').
    segm_idx = df[['segm_idx', 'collection']].drop_duplicates()

    for index, row in tqdm(segm_idx.iterrows(), total=segm_idx.shape[0]):
        segment = row['segm_idx']

        ## - Get id_collection, id_tablet and id_view from DB
        collection_ref = row['collection']
        coll_search_query = f"""
                             SELECT id_collection FROM collection_ref
                              WHERE collection_name = '{str(collection_ref)}';
                             """
        id_collection = postgres_execute_search_query(coll_search_query)

        tablet_ref = df.loc[((df['segm_idx'] == segment)\
            & (df['collection'] == collection_ref)), 'tablet_CDLI'].unique()
        tab_search_query = f"""
                            SELECT id_tablet FROM tablet_ref
                             WHERE tablet_name = '{str(tablet_ref[0])}';
                            """
        id_tablet = postgres_execute_search_query(tab_search_query)

        view_ref = df.loc[((df['segm_idx'] == segment)\
            & (df['collection'] == collection_ref)), 'view_desc'].unique()
        view_search_query = f"""
                             SELECT id_view FROM view_ref
                              WHERE view_name = '{str(view_ref[0])}';
                             """
        id_view = postgres_execute_search_query(view_search_query)

        ## - Get BBox ans Scale from tablet_segments csv
        for file in CSV_FILES:
            if any(substring in file for substring in\
                  [f"tablet_segments_{collection_ref}"]):
 
                df_segment = pd.read_csv(file)

                bbox = df_segment.loc[df_segment['segm_idx']\
                                       == segment, 'bbox'].unique()
                scale = df_segment.loc[df_segment['segm_idx']\
                                        == segment, 'scale'].unique()

                ## - Insert
                query = f"""
                        INSERT INTO segment_ref (segment_idx, bbox_segment, 
                                                scale, id_collection, 
                                                id_tablet, id_view)
                        VALUES ('{segment}', '{bbox[0]}', {scale[0]}, 
                                 {id_collection[0]}, {id_tablet[0]}, 
                                 {id_view[0]})
                        """

                postgres_execute_insert_query(query)


def insert_mzl_ref(mzl_dict: dict) -> None:
    ## - Get the train_label if exist
    for file in CSV_FILES:
        if any(substring in file for substring in [f"bbox"]):
            df_bbox = pd.read_csv(file)
            control_df = df_bbox[df_bbox['mzl_label']\
                                  == mzl_dict['mzl_number']].head(1)

            if not control_df.empty:
                train_label = control_df['train_label'].values[0]
            else : 
                train_label = 'NULL'
            break

    ## - Complete dict when no information on some glyph (ex: 48, 58...)
    if 'name' not in mzl_dict: mzl_dict['name'] = ''
    if 'glyph' not in mzl_dict: mzl_dict['glyph'] = ''
    if 'phonetic' not in mzl_dict or not mzl_dict['phonetic']:
        mzl_dict['phonetic'] = 'NULL'

    ## - Insert
    query = f"""
            INSERT INTO mzl_ref (mzl_number, train_label, 
                                glyph_name, glyph, glyph_phonetic)
                 VALUES ({mzl_dict['mzl_number']}, {train_label}, 
                         '{mzl_dict['name']}', '{mzl_dict['glyph']}',
                         {f"ARRAY {mzl_dict['phonetic']}"
                          if mzl_dict['phonetic'] != 'NULL' else 'NULL'});
            """

    postgres_execute_insert_query(query)


def insert_annotation_ref(df):
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):

        ## - Get id_segment from DB,
        segment_search_query = f"""
                SELECT sr.id_segment FROM segment_ref sr
                  JOIN collection_ref cr ON sr.id_collection = cr.id_collection
                 WHERE cr.collection_name = '{row['collection']}'
                   AND sr.segment_idx = {row['segm_idx']};
        """
        id_segment = postgres_execute_search_query(segment_search_query)

        ## - Insert
        query = f"""
                 INSERT INTO annotation_ref(bbox, relative_bbox,
                                            mzl_number, id_segment)
                      VALUES ('{row['bbox']}', '{row['relative_bbox']}', 
                              {row['mzl_label']}, {id_segment[0]})
                 """
        postgres_execute_insert_query(query)


def insert_reveal(df):
    ## - Get id_tablet
    tablet_name = df['tablet_CDLI'].unique()
    tablet_view = df[['tablet_CDLI', 'view_desc']].drop_duplicates()

    for tablet in tqdm(tablet_name):
        tab_search_query = f"""
            SELECT id_tablet FROM tablet_ref
                WHERE tablet_name = '{tablet}';
            """
        id_tablet = postgres_execute_search_query(tab_search_query)

        ## - Get id_view
        for index, row in tablet_view[tablet_view['tablet_CDLI']\
                                       == tablet].iterrows():
            view_ref = row['view_desc']
            view_search_query = f"""
                                    SELECT id_view FROM view_ref
                                    WHERE view_name = '{view_ref}';
                                    """
            id_view = postgres_execute_search_query(view_search_query)

            ## - Insert
            query = f"""
                    INSERT INTO reveal(id_tablet, id_view)
                        VALUES ({id_tablet[0]}, {id_view[0]})
                    """
            postgres_execute_insert_query(query)
