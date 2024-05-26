#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================
# Configuration file for the connection to DB
# ==============================================================================



def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations, which are used
    by the following method : psycopg2.connect()
    """

    config = {
        ## -- Local Configuration -- ##
        # "host" : "localhost",
        # "database" : "aissyr",
        # "user" : "DIGMIR",
        # "password" : "m3s_!",
        # "port" : "5432"

        ## -- Heroku Configuration -- ##
        "host" : "",
        "database" : "",
        "user" : "",
        "password" : "",
        "port" : "" ## -- Default port for PostgreSQL
    }

    return config


def get_csv_path() -> dict:

    path = {
        "annotation" : 'data/annotations/',
        "segment" : 'data/segments/'
    }

    return path


def get_img_path() -> dict:

    path = {
        "cdli" : 'data/images/CDLI/',
        "vat" : 'data/images/VAT/'
    }

    return path


def get_json_path() -> dict:

    path = {
        "mzl_ref" : 'data/neo_assyrian_info.json'
    }
    return path
