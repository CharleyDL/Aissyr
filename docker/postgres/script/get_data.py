import pandas as pd
import psycopg2

## - Personal librairies
import config


from IPython.display import display

CONFIG = config.get_db_config()



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
            # print("PostgreSQL connection is closed")


if __name__ == '__main__':

    PARAMS = ['train', 'test']
    COLUMNS = ['tablet_CDLI', 'mzl_number', 'train_label', 
               'bbox_segment', 'bbox_glyph']

    df_train = pd.DataFrame()
    df_test = pd.DataFrame()

    for param in PARAMS:
        query = f"""
                SELECT
                    tr.tablet_name AS tablet_CDLI,
                    sr.bbox_segment,
                    ar.relative_bbox AS bbox_glyph,
                    mr.mzl_number,
                    mr.train_label
                FROM segment_ref sr
                JOIN tablet_ref tr ON sr.id_tablet = tr.id_tablet
                JOIN view_ref vr ON sr.id_view = vr.id_view
                JOIN collection_ref cr ON sr.id_collection = cr.id_collection
                JOIN annotation_ref ar ON sr.id_segment = ar.id_segment
                JOIN mzl_ref mr ON ar.mzl_number = mr.mzl_number
                WHERE tr.set_split = '{param}';
                """

        result = pd.DataFrame(postgres_execute_search_query(query),
                              columns=COLUMNS)

        if param == 'train':
            df_train = result
        elif param == 'test':
            df_test = result


    display(df_train.head(2))

