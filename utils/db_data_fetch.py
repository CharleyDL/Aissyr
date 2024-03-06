#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By : Charley ∆. Lebarbier
# Date Created : Wednesday 31 Jan. 2024
# ==============================================================================
# Script for fetching bounding box annotation data and images from a PostgreSQL 
# database.
# ==============================================================================

import pandas as pd
import psycopg2
import sys

sys.path.append("../docker/postgres/script/")
import config as cfg


CONFIG = cfg.get_db_config()


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
        result = cursor.fetchall()

        # print(f"{result}")

        return result

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")


def fetch_data_bbox_annotation(set_param: str) -> pd.DataFrame:
    """
    Fetches bounding box annotation data from the Postgres database.

    Parameters:
    -----------
    - set_param (str, required): Set split parameter specifying 
    the set to fetch (train or test).

    Returns:
    --------
    - pd.DataFrame: DataFrame containing the fetched data 
    with the following columns:
        - tablet_CDLI (str): Tablet name - CDLI reference.
        - bbox_segment (str): Bounding box segment -> resizing the tablet 
                              on specific segment.
        - bbox_glyph (str): Bounding box glyph.
        - mzl_number (int): MZL number refering to the glyph detected in bbox
        - train_label (str): MZL training label.
    """
    COLUMNS = ['tablet_name', 'bbox_glyph', 'mzl_label']

    query = f"""
            SELECT 
                CONCAT(tablet_name, 
                       CASE 
                           WHEN vr.view_name = 'Obv' THEN '_o' 
                           ELSE '_r' 
                       END) AS tablet_name,
                ar.relative_bbox AS bbox_glyph,
                ar.mzl_number AS mzl_label
            FROM tablet_ref tr
            JOIN segment_ref sr ON tr.id_tablet = sr.id_tablet
            JOIN annotation_ref ar ON sr.id_segment = ar.id_segment
            JOIN view_ref vr ON sr.id_view = vr.id_view
            WHERE tr.set_split = '{set_param}';
            """

    result = pd.DataFrame(postgres_execute_search_query(query),
                          columns=COLUMNS)
    return result


def fetch_image(set_param: str) -> pd.DataFrame:
    COLUMNS = ['tablet_name', 'tablet_picture', 'bbox_segment']

    query = f"""
            SELECT 
                CONCAT(tr.tablet_name, 
                    CASE 
                        WHEN vr.view_name = 'Obv' THEN '_o' 
                        ELSE '_r' 
                    END) AS tablet_name,
                tr.picture AS tablet_picture,
                sr.bbox_segment
            FROM tablet_ref tr
            JOIN segment_ref sr ON tr.id_tablet = sr.id_tablet
            JOIN view_ref vr ON sr.id_view = vr.id_view
            WHERE tr.set_split = '{set_param}';
            """

    result = pd.DataFrame(postgres_execute_search_query(query),
                          columns=COLUMNS)
    return result
