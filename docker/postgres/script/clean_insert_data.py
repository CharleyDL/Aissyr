#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 12 Jan. 2024
# ==============================================================================
# Script to clean 'bbox_annotations' dataset and insert its data into a 
# PostgreSQL database. MAIN TASKS : Loading CSV files, applying data cleaning 
# strategies, and send data for importation to 'postgres_insert_utils' 
# (piu) script.
# ==============================================================================

import base64
import glob
import json
import os
import pandas as pd

## - Personal librairies
import config
import postgres_insert_utils as piu


CSV_FOLDER_PATH = config.get_csv_path()
# JSON_FILES = config.get_json_path()

# with open(JSON_FILES['mzl_ref']) as mzl_json:
#     MZL_DATA = json.load(mzl_json)



def insert_bbox_annotations_file(df: pd.DataFrame, label_file) -> None:
    """
    Insert 'bbox_annotations' data into PostgreSQL tables :
    view_ref, collection_ref, tablet_ref, and segment_ref.

    Parameter:
    -----------
    df (DataFrame, required): DataFrame containing 'bbox_annotations' data
    label_file (str, required): Define if file is the train or test set
    """
    # piu.insert_view_ref(df)
    # piu.insert_collection_ref(df)
    # piu.insert_tablet_ref(df, label_file)
    # piu.insert_segment_ref(df)

    # for mzl_number in MZL_DATA:
    #     piu.insert_mzl_ref(mzl_number)

    piu.insert_annotation_ref(df)


def df_bbox_annotations(df: pd.DataFrame, label_file) -> None:
    """
    Apply cleaning strategies to the 'bbox_annotations' DataFrame before 
    insertion.

    Parameter:
    -----------
    df (pd.DataFrame, required): DataFrame containing 'bbox_annotations' 
    data needed to be cleaned and inserted into the Postgres Database.
    """

    ## - Delete rows with segm_idx -1 and tablets P336663b, K09237Vs
    df.drop(df[(df['segm_idx'] == -1)].index, inplace=True)
    df.drop(df[(df['tablet_CDLI'] == "P336663b") 
               | (df['tablet_CDLI'] == "K09237Vs")].index, inplace=True)

    df.reset_index(drop=True, inplace=True)

    insert_bbox_annotations_file(df, label_file)


def get_files_path(dir_path: dict) -> list:
    """
    Get a list of all file paths from specified directories.

    Parameter:
    -----------
    dir_path (dict, required): A dictionary containing directory names 
    as keys and their paths as values.

    Return:
    --------
    list: A list containing the full paths of all files from specific 
    directories.

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




if __name__ == '__main__':
    files = get_files_path(CSV_FOLDER_PATH)

    for file in files:
        ## - Filter to get only bbox_annotations files
        if any(substring in file for substring in ["bbox_annotations_"]):
            df = pd.read_csv(file)
            if (any(substring in file for substring in ["train"])):
                df_bbox_annotations(df, "train")
            else:
                df_bbox_annotations(df, "test")
