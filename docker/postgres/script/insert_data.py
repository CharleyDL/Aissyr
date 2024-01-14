#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 12 Jan. 2024
# ==============================================================================
# Script to clean dataset and insert data into Postgres DB
# ==============================================================================

## - General libraries
import os
import pandas as pd
import psycopg2

## - Personal libraries
import config


CONFIG = config.get_db_config()
PATH = config.get_path()


def connect_test():
    """test de connection sur la db"""

    try:
        db = psycopg2.connect(**CONFIG)
        cursor = db.cursor()

        postgre_query = """
                           SELECT table_name 
                             FROM information_schema.tables 
                            WHERE table_schema='public';
                        """
        cursor.execute(postgre_query)
        result = cursor.fetchall()

        print(result)

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            print("PostgreSQL connection is closed")



def df_annotation(df: pd.DataFrame) -> None:
    """Apply clean strategy to get the real insert df"""

    ## - Delete row with segm_idx -1 and tablets P336663b, K09237Vs
    df.drop(df[(df['segm_idx'] != -1) 
               & ((df['tablet_CDLI'] == "P336663b") 
                  | (df['tablet_CDLI'] == "K09237Vs"))].index, inplace=True)

    ## - Reindex the df
    df.reset_index(drop=True, inplace=True)
    print(df)


def df_segment(df: pd.DataFrame) -> None:
    

    print("SEGMENT")


def load_dataset(csv_path: str) -> None:
    """Load dataset to clean before import in db"""
    print(csv_path)
    df = pd.read_csv(csv_path)

    ## - Verification to apply the right clean-insert strategy
    if "bbox_annotations" in csv_path: df_annotation(df)
    elif "tablet_segments" in csv_path: df_segment(df)
    else: print("File not supported")


def get_files_path(dir_path: dict) -> list:
    """
    Get a list of file paths from specified directories.

    Parameters:
    -----------
    dir_path (dict): A dictionary containing directory names as keys and their paths as values.

    Returns:
    --------
    list: A list containing the full paths of all files in the specified directories.

    Example:
    --------
    >>> directories = {"a": "/path/to/a", "b": "/path/to/b"}
    >>> files = get_files_path(directories)
    >>> print(files)
    ['/path/to/a/file1.txt', '/path/to/a/file2.txt', '/path/to/segments/b.txt', ...]
    """
    files_path = []

    for dir in dir_path.values():
        for filename in os.listdir(dir):
            files_path.append(os.path.join(dir, filename))

    return files_path




if __name__ == '__main__':
    files = get_files_path(PATH)

    for file in files:
        load_dataset(file)
