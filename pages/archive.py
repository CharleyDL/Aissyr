#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 29 Apr. 2024
# ==============================================================================

import streamlit as st

import utils.functions as fct


## ------------------------------- SETUP PAGE ------------------------------- ##

st.set_page_config(page_title='AISSYR',
                   page_icon='asset/fav32.png',
                   layout='wide')

fct.check_session()


## --------------------------------- HEADER --------------------------------- ##

st.page_link('pages/main_page.py',
            label="Go back to Main Page",
            icon='⬅')

st.header('ARCHIVE PAGE')
st.markdown('----')

tabDet, tabLab = st.tabs(['Detection', 'Labelisation'])

## --------------------------------- SIDEBAR -----=-------------------------- ##

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

    for i in range(31):
        fct.space()

    cols = st.columns([1,1,1])

    with cols[1]:
        logout_button = st.button("Logout")
        if logout_button:
            fct.logout()


## ----------------------------- TAB DETECTION ------------------------------ ##

with tabDet:
    detection_dict = fct.get_archives_classification()

    if detection_dict:
        fct.display_archives_classification(detection_dict)
    else:
        st.write('No detection archive to display')


## --------------------------- TAB LABELISATION ----------------------------- ##

with tabLab:
    labelisation_dict = fct.get_archives_labelisation()

    if labelisation_dict:
        fct.display_archives_labelisation(labelisation_dict)
    else:
        st.write('No labelisation archive to display')
