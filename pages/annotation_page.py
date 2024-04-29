#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import streamlit as st
import utils.functions as fct


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR',
                   page_icon='asset/fav32.png',
                   layout='wide')

fct.check_session()


## ------------------------------- HEADER  ---------------------------------- ##

st.page_link('pages/main_page.py',
            label="Go back to Main Page",
            icon='⬅')

st.header('LABELISATION PAGE')
st.markdown('----')


## ------------------------------ SIDEBAR ----------------------------------- ##

with st.sidebar:
    st.markdown(
    """
    <style>
        [data-testid=stImage]{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
    </style>
    """, unsafe_allow_html=True
    )
    st.image('asset/logo_aissyr_S.png')

    for i in range(2):
        fct.space()

    st.write("""
             <h3 style='text-align: center;'>🧰 TOOLKIT</h3>
             """, unsafe_allow_html=True)

    fct.space()

    st.page_link('pages/detect_page.py',
                 label="Detect Glyphs",
                 icon='🔍')

    st.page_link('pages/annotation_page.py',
                 label="Label Glyphs",
                 icon='🏷️')

    st.page_link('pages/archive.py', 
                 label="Archive",
                 icon='📚')

    for i in range(8):
        fct.space()
    st.markdown('----')

    st.write("""
             <h3 style='text-align: center;'> UPLOAD IMAGE</h3>
             """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader('upload img',
                                      type=["jpg", "jpeg"],
                                      label_visibility='hidden')

    for i in range(2):
        fct.space()

    cols = st.columns([1,1,1])

    with cols[1]:
        logout_button = st.button("Logout")
        if logout_button:
            fct.logout()

## -------------------------------------------------------------------------- ##

if uploaded_file is not None:
    fct.clear_session_state('uploaded_file')
    st.session_state.upload_file = uploaded_file

    fct.annotation_setup(uploaded_file)







# img_path = os.path.join(img_dir, img_file_name)
# im = ImageManager(img_path)
# img = im.get_img()
# resized_img = im.resizing_img()
# resized_rects = im.get_resized_rects()
# rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

# def annotate():
#     im.save_annotation()
#     image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
#     if image_annotate_file_name not in st.session_state["annotation_files"]:
#         st.session_state["annotation_files"].append(image_annotate_file_name)
#     next_annotate_file()

# if rects:
#     st.button(label="Save", on_click=annotate)
#     preview_imgs = im.init_annotation(rects)

#     for i, prev_img in enumerate(preview_imgs):
#         prev_img[0].thumbnail((200, 200))
#         col1, col2 = st.columns(2)
#         with col1:
#             col1.image(prev_img[0])
#         with col2:
#             default_index = 0
#             if prev_img[1]:
#                 default_index = labels.index(prev_img[1])

#             select_label = col2.selectbox(
#                 "Label", labels, key=f"label_{i}", index=default_index
#             )
#             im.set_annotation(i, select_label)
