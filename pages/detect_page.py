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

st.header('DETECT PAGE')
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

    st.page_link('pages/labelisation_page.py',
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

## - clear session state for correct page
fct.clear_session_state('correct_label')
fct.clear_session_state('del_label')
fct.clear_session_state('rects_correct')

## - Upload file to classify glyphs
if uploaded_file is not None:
    fct.clear_session_state('uploaded_file')
    st.session_state.upload_file = uploaded_file

    fct.classification_setup(uploaded_file)


## ------------------------------ SESSION STATE ----------------------------- ##

st.session_state.disable_btns_correct_page = True       # reset button state
                                                        # of the correct page
