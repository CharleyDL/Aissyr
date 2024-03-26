#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================


import streamlit as st
import utils.functions as fct

## ----------------------------- SETUP PAGE --------------------------------- ##

st.page_link('pages/main_page.py', 
            label="Go back to Main Page",
            icon='⬅')


## ------------------------------ PAGE CONTENT ------------------------------ ##

st.header('ARCHIVE PAGE')
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

    st.page_link('pages/detect.py', 
                 label="Detect Glyphs",
                 icon='🔍')

    st.page_link('pages/annotation.py', 
                 label="Label Glyphs",
                 icon='🏷️')

    st.page_link('pages/archive.py', 
                 label="Archive",
                 icon='📚')

## -------------------------------------------------------------------------- ##
