#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import streamlit as st

import utils.functions as fct

from streamlit_extras.row import row
from streamlit_img_label.manage import ImageManager


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR',
                   page_icon='asset/fav32.png',
                   layout='wide')

fct.check_session()
fct.button_del_page()

## - Load glyphs information
ALL_MZL = fct.all_mzl_info('list')


## ------------------------------- HEADER  ---------------------------------- ##

st.page_link('pages/labelisation_page.py',
            label="Go back to Labelisation Page",
            icon='⬅')

st.header('SELECT LABELS')
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

    for i in range(32):
        fct.space()

    cols = st.columns([1,1,1])

    with cols[1]:
        logout_button = st.button("Logout")
        if logout_button:
            fct.logout()


## ------------------------------ MAIN PAGE --------------------------------- ##

## - Setup Rows Configuration
rowOption = row(8, gap='small')
rowImgDet = row([0.3, 0.7], gap='small', vertical_align='center')

## - Buttons
save_button = rowOption.button(label="Save Label", 
                               key="save_label",
                               on_click=fct.disable_btns_save,
                               disabled=st.session_state.disable_btns_save)

## - Display glyphs and selectbox to correct if needed
if not save_button:
    if st.session_state.zip_labelisation:

        for i, result in enumerate(st.session_state.zip_labelisation):
            rowImgDet.image(result[0])
            select_label = rowImgDet.selectbox("Label",
                            ALL_MZL, 
                            key=f"label_{i}",
                            index=None,
                            placeholder='-',
                            label_visibility='hidden',
                            on_change=fct.update_labelisation,
                            args=(i,))

else:
    st.write("""
    <h4 style='text-align: center;'>
        Summary
    </h4>
        """, unsafe_allow_html=True)

    rowImgDet = row([0.3, 0.7], gap='small')

    _cL, colC, _cR = st.columns([1,2,1])
    with colC:
        fct.space()

        rowCorrectGlyph = row([0.3, 0.7], gap='small')
        for i, result in enumerate(st.session_state.zip_labelisation):
            rowCorrectGlyph.image(result[0])
            rowCorrectGlyph.write(f"""
            <p style='padding-top: 24px;
                    font-size: 20px;'>
            <b>
                {result[1][0]}
                <span style='margin-left: 16px;'>&nbsp;</span>
                {result[1][1]} - {result[1][2]}
            </b>
            </p>
            """, unsafe_allow_html=True)

    ## -Send Labelisation to the API
    img = ImageManager(st.session_state.upload_file).get_img()
    img_name = st.session_state.upload_file.name

    width, height = img.size
    bbox_img = [0, 0, width, height]    # Need for the annotation save not inference

    # - Check if the user is in DEMO mode
    if st.session_state.f_name == 'DEMO':
        st.toast(f"""This is a demo version, 
             the data is not saved in the database.""", icon='🚫')
    else:
        ## -- Send Corrected Glyphs to the API and display the message
        annot_results = fct.save_labelisation(img_name,
                            img,
                            bbox_img,
                            st.session_state.rects_annotation,
                            st.session_state.zip_labelisation)

        for i, result in enumerate(annot_results):
            if result['result']:
                    st.toast(result['message'], icon='✅')
            else:
                st.toast(result['message'], icon='🚫')
