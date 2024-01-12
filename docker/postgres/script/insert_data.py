#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 12 Jan. 2024
# ==============================================================================
# Script to clean dataset and insert data into Postgres DB
# ==============================================================================

## - General libraries
import pandas as pd
import psycopg2

## - Personal libraries
import config


CONFIG = config.get_db_config()



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




def load_dataset(folder_path: str, ):
    """Load dataset to clean before import in db"""

    df = pd.read_csv()



if __name__ == '__main__':
    pass