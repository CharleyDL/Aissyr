#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import bcrypt
import mlflow.pyfunc
import numpy as np
import psycopg2
import streamlit as st
import utils.functions as fct

from PIL import Image
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager
from streamlit_extras.row import row


## -------------------------- POSTGRESQL DATABASE --------------------------- ##

def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations, which are used
    by the following method : psycopg2.connect()
    """

    config = {
        ## -- Local Configuration -- ##
        "host" : "localhost",
        "database" : "neo_aissyr",
        "user" : "DIGMIR",
        "password" : "m3s_!",
        "port" : "5432"
    }

    return config


def postgres_execute_insert_new_user(credentials: list) -> None:
    """
    Execute an INSERT a new user in a PostgreSQL database.

    Parameter:
    -----------
    query (str, required): The SQL query to be executed.
    """
    title, first_name, last_name, email, password = credentials

    query= f"""
        INSERT INTO account_user (title, last_name, first_name, email, pwd_hash)
        SELECT %s, %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM account_user WHERE email = %s);
        """

    try:
        db = psycopg2.connect(**get_db_config())
        cursor = db.cursor()
        cursor.execute(query,
                       (title, last_name, first_name, email, password, email)
        )

        if cursor.rowcount > 0:
            db.commit()
            # print("Insertion Done")
            return True
        else:
            db.rollback()
            return False
 
    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            # print("PostgreSQL connection is closed")


def postgres_execute_login(credentials: list) -> tuple:
    """
    Execute a search query in a PostgreSQL database.

    Parameters:
    -----------
    query (str, required): The SQL query to be executed.

    Return:
    --------
    tuple: Query result
    """

    email, password = credentials

    query = f"""
        SELECT pwd_hash FROM account_user
        WHERE email = %s;
        """

    try:
        db = psycopg2.connect(**get_db_config())
        cursor = db.cursor()
        cursor.execute(query,(email,))
        result = cursor.fetchone()

        if result is not None:
            hashed_password = result[0].tobytes()
            if check_bcrypt(password, hashed_password):
                return True
            else:
                st.toast("Incorrect password", icon='🔐')
                print("Incorrect password")
        else:
            st.toast("User not found", icon='❓')

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            # print("PostgreSQL connection is closed")


def postgres_execute_get_mzl() -> list:
    """
    Get MZL information from DB

    Parameters:
    -----------
    query (str, required): The SQL query to be executed.

    Return:
    --------
    List: MZL Information on format : [482 - 𒀤 AL×HA]
    """
    query = f"""
        SELECT mzl_number, glyph, glyph_name 
        FROM mzl_ref;
        """

    try:
        db = psycopg2.connect(**get_db_config())
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        mzl_list = []
        for index, item in enumerate(result, start=1):
            formatted_item = f"{index}. {'  '.join(str(e) for e in item[1:])}"
            mzl_list.append(formatted_item)

        return mzl_list

    except (Exception, psycopg2.Error) as error:
        print(f"Failed : {error}")

    finally:
        if db:
            cursor.close()
            db.close()
            # print("PostgreSQL connection is closed")


## ----------------------------- BCRYPT HASHING ----------------------------- ##

def hash_bcrypt(plain_text: str) -> bytes:
    plain_text_bytes = plain_text.encode()
    return bcrypt.hashpw(plain_text_bytes, bcrypt.gensalt(12))


def check_bcrypt(plain_text: str, hashed_password: bytes) -> bool:
    try:
        plain_text_bytes = plain_text.encode()
        return bcrypt.checkpw(plain_text_bytes, hashed_password)
    except:
        return False


## --------------------------- STREAMLIT UTILITIES -------------------------- ##

def clear_cache(key: str) -> None:
    st.session_state.pop(key)


def space() -> None:
    """Add a break line"""
    st.markdown("""<style> <br /> </style>""", unsafe_allow_html=True)


## --------------------------------- IMAGES --------------------------------- ##

def extract_and_resize(image, output_size=(128, 128)):
    if image.mode != 'RGB':
        image = image.convert('RGB')

    resized_roi = image.resize(output_size, resample=Image.LANCZOS)

    return resized_roi

## ------------------------------- DETECTION -------------------------------- ##

@st.cache_resource()
def load_model():
    model_id = 'runs:/d104fc5e1dd8470a8dde5b0c7a760814/model'
    loaded_model = mlflow.pyfunc.load_model(model_id)
    return loaded_model


def detect_glyphs(img):
    # model = load_model()

    # Preprocess the image

    # Detect the glyphs
    # res = model.predict(img)
    # res = "𒀸 AŠ"
    # res = "𒀸𒀸 2"
    res = "𒀸𒀸𒀸 3"

    

    return res


def init_detect(img_path):
    if 'preview_imgs' not in st.session_state:
        st.session_state.preview_imgs = []

    if 'res_detect' not in st.session_state:
        st.session_state.res_detect = []

    if 'zip_detect' not in st.session_state:
        st.session_state.zip_detect = []

    preview_imgs = []

    col1, col2 = st.columns(2)
    with col1:
        im = ImageManager(img_path)
        resized_img = im.resizing_img()
        img = im.get_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

        detect_button = st.button(label="Detect")

    with col2:
        preview_imgs = im.init_annotation(rects)

        rowImgDet = row(2, gap='medium')
        tmp_img = st.empty()

        for i, prev_img in enumerate(preview_imgs):
            resize_prev_img = extract_and_resize(prev_img[0])

            colImg, colDet = st.columns(2)
            with colImg:
                tmp_img.image(resize_prev_img)

        if detect_button:
            res = detect_glyphs(resize_prev_img)

            st.session_state.preview_imgs.append(resize_prev_img)
            st.session_state.res_detect.append(res)
            st.session_state.zip_detect.append((resize_prev_img, res))

            tmp_img.empty()

        for i, result in enumerate(st.session_state.zip_detect):
            rowImgDet.image(result[0])
            rowImgDet.write(f"""
                            <h4 style='padding-top: 48px;'>---- {result[1]}</h4>
                            """, unsafe_allow_html=True)






## ------------------------------- ANNOTATION ------------------------------- ##

def annotate():
    print("Detecting")
    # im.save_annotation()
    # image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
    # if image_annotate_file_name not in st.session_state["annotation_files"]:
    #     st.session_state["annotation_files"].append(image_annotate_file_name)
    # next_annotate_file()

def annotate(img_path):

    im = ImageManager(img_path)
    img = im.get_img()
    resized_img = im.resizing_img()
    resized_rects = im.get_resized_rects()
    rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

    labels = fct.postgres_execute_get_mzl()

    st.button(label="Labeled", on_click=annotate)

    preview_imgs = im.init_annotation(rects)

    for i, prev_img in enumerate(preview_imgs):
        prev_img[0].thumbnail((200, 200))
        col1, col2 = st.columns(2)
        with col1:
            col1.image(prev_img[0])
        with col2:
            default_index = 0
            if prev_img[1]:
                default_index = labels.index(prev_img[1])

            select_label = col2.selectbox(
                "Label", labels, key=f"label_{i}", index=default_index
            )
            im.set_annotation(i, select_label)





















## saving for init_detect

    # with col2:
    #     ## Test pour afficher à droite
    #     st.session_state.preview_imgs = im.init_annotation(rects)

    #     for i, prev_img in enumerate(st.session_state.preview_imgs):
    #         resize_prev_img = extract_and_resize(prev_img[0])

    #         col1, col2 = st.columns(2)
    #         col1.image(resize_prev_img)

    #         if detect_button:
    #             print(f"state preview imgs : {st.session_state.preview_imgs}")

    #             for pi in st.session_state.preview_imgs:
    #                 st.session_state.res_detect.append(detect_glyphs(resize_prev_img))

    #             col2.write(f"--- {st.session_state.res_detect[i]}")


    # with col2:
    #     preview_imgs = im.init_annotation(rects)

    #     colImg, colDet = st.columns(2)
    #     for i, prev_img in enumerate(preview_imgs):
    #         resize_prev_img = extract_and_resize(prev_img[0])
    #         print(f"resize_prev_img : {resize_prev_img}")
    #         colImg.image(resize_prev_img)

    #         if detect_button:
    #             res = detect_glyphs(resize_prev_img)
    #             st.session_state.preview_imgs.append(resize_prev_img)
    #             st.session_state.res_detect.append(res)
    #             st.session_state.zip_detect.append((resize_prev_img, res))

    #             print(f"state preview imgs : {st.session_state.preview_imgs}")
    #             print(f"state res detect : {st.session_state.res_detect}")
    #             print(f"state zip : {st.session_state.zip_detect}")

    #         # for detected_img, result in enumerate(st.session_state.zip_detect):
    #         #     colDet.write(f"--- {result[i]}")
            

        ## version 1 fonctionnel moins bien
    # with col2:
    #     preview_imgs = im.init_annotation(rects)
    #     rowImgDet = row(2, vertical_align='center', gap='medium')

    #     # colImg, colDet = st.columns(2)
    #     for i, prev_img in enumerate(preview_imgs):
    #         resize_prev_img = extract_and_resize(prev_img[0])

    #         # colImg.image(resize_prev_img)
    #         rowImgDet.image(resize_prev_img)

    #     if detect_button:
    #         res = detect_glyphs(resize_prev_img)
    #         print(f"resize : {resize_prev_img}")

    #         st.session_state.preview_imgs.append(resize_prev_img)
    #         st.session_state.res_detect.append(res)
    #         st.session_state.zip_detect.append((resize_prev_img, res))

    #         # rowImgDet.write(f"--- {res}")

    #     for i, result in enumerate(st.session_state.zip_detect):
    #         # print(i, result)
    #         # colDet.write(f"--- {result[1]}")
    #         rowImgDet.image(result[0])
    #         rowImgDet.write(f"--- {result[1]}")


    ## - Version 2 fonctionnel mais sans le temps reel
    # with col2:
    #     preview_imgs = im.init_annotation(rects)
    #     rowImgDet = row(2, vertical_align='center', gap='medium')

    #     for i, prev_img in enumerate(preview_imgs):
    #         resize_prev_img = extract_and_resize(prev_img[0])

    #     if detect_button:
    #         res = detect_glyphs(resize_prev_img)
    #         print(f"resize : {resize_prev_img}")

    #         st.session_state.preview_imgs.append(resize_prev_img)
    #         st.session_state.res_detect.append(res)
    #         st.session_state.zip_detect.append((resize_prev_img, res))

    #     for i, result in enumerate(st.session_state.zip_detect):
    #         rowImgDet.image(result[0])
    #         rowImgDet.write(f"--- {result[1]}")