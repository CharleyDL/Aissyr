#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 12 Jan. 2024
# ==============================================================================
# Script to clean dataset and insert data into Postgres DB
# ==============================================================================

## - General libraries
import base64
import glob
import os
import pandas as pd
import psycopg2

## - Personal libraries
import config
import postgres_insert_utils as piu



CSV_FOLDER_PATH = config.get_csv_path()






def insert_annotation(df: pd.DataFrame) -> None:
    ## - insert view_ref in view_ref table
    # piu.insert_view_ref(df)

    ## - insert collection in collection_ref table
    # piu.insert_collection_ref(df)

    ## - insert tablet_ref in tablet_ref table
    # piu.insert_tablet_ref(df)

    ##------------------------------------##
    ## - insert segment_ref in segment_ref table
    piu.insert_segment_ref(df)

    ## - récupérer segment et la collection
    # print(segm_idx)

    # - ouvrir le table_segment correspondant à la collection

    # - récupérer les infos en question pour envoyer dans l'insert



    # df_segment()





"""
def insert_segment(df: pd.DataFrame) -> None:
    ## - insert segment_ref
    # piu.insert_segment_ref(df)
    pass
"""





def df_annotation(df: pd.DataFrame) -> None:
    """Apply clean strategy to get the real insert df"""

    ## - Delete rows with segm_idx -1 and tablets P336663b, K09237Vs
    df.drop(df[(df['segm_idx'] == -1)].index, inplace=True)
    df.drop(df[(df['tablet_CDLI'] == "P336663b") 
               | (df['tablet_CDLI'] == "K09237Vs")].index, inplace=True)

    ## - Reindex the df
    df.reset_index(drop=True, inplace=True)
    # print(df)

    insert_annotation(df)


def df_segment(df: pd.DataFrame) -> None:
    """Apply clean strategy to get real insert df"""

    ## - Delete rows with no value in view_desc and P336663b / K09237V tablets
    df.drop(df[df['view_desc'].isnull()].index, inplace=True)
    df.drop(df[(df['tablet_CDLI'] == "P336663b") 
               | (df['tablet_CDLI'] == "K09237Vs")].index, inplace=True)

    ## - Reindex the df
    df.reset_index(drop=True, inplace=True)
    # print(df)

    # insert_segment(df)


def get_files_path(dir_path: dict) -> list:
    """
    Get a list of all file paths from specified directories.

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


def get_image(ref_name: str, img_folder_path: dict) -> base64:
    """
    Retrieve and encode an image associated.

    Parameters:
    -----------
    - ref_name (str, required): Reference name to retrieve the image for.
    - img_folder_path (dict, required): the folder image path 

    Return:
    --------
    - str: Base64-encoded string representation of the binary image data.

    Exemple:
    --------
    >>> directories = {"a": '/path/to/img_folder_a', "b": '/path/to/img_folder_b'}
    >>> img_encode = get_image("my_pic", directories)
    >>> print(img_encode)
    "jl1eKA2FfNnjx5cnKBPzL8V/8AnJPy95J8q/....."
    """

    ## - Get Image Path
    for path in img_folder_path.values():
        img_path = glob.glob(f'{path}{ref_name}*')
        if img_path: break

    ## - Convert Image to binaryData for BYTEA data type in db
    with open(img_path[0], 'rb') as img:
        img_data = img.read()
    binary_img = base64.b64encode(img_data).decode('utf-8')

    return binary_img


def load_dataset(csv_path: str) -> None:
    """Load dataset to clean before import in db"""
    print(csv_path)
    df = pd.read_csv(csv_path)

    ## - Verification to apply the right clean-insert strategy
    if "bbox_annotations" in csv_path: df_annotation(df)
    # elif "tablet_segments" in csv_path: df_segment(df)
    # else: print("File not supported")




if __name__ == '__main__':
    files = get_files_path(CSV_FOLDER_PATH)

    for file in files:
        ## - Filter to get only bbox_annotation file
        if any(substring in file for substring in ["bbox"]):
            load_dataset(file)
