#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import streamlit as st

import utils.functions as fct

from streamlit_extras.row import row


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR',
                   page_icon='asset/fav32.png',
                   layout='wide')

fct.check_session()
fct.button_del_page()

## - Load glyphs information
ALL_MZL = fct.all_mzl_info('list')


## ------------------------------- HEADER  ---------------------------------- ##

st.page_link('pages/detect.py',
            label="Go back to Detect Page",
            icon='⬅')

st.header('CORRECT LABELS')
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
rowImgDet = row([0.3, 0.5, 0.2], gap='small', vertical_align='center')

## - Buttons
validate = rowOption.button(label="Validate", 
                            on_click=fct.disable_btns_correct_page, 
                            disabled=not st.session_state.disable_btns_correct_page)

save_button = rowOption.button(label="Save Label", key="save_correct_page",
                        disabled=st.session_state.disable_btns_correct_page)

## - Display glyphs and selectbox to correct if needed
if not validate:
    if st.session_state.zip_detect:
        for i, result in enumerate(st.session_state.zip_detect):
            rowImgDet.image(result[0])
            new_label = rowImgDet.selectbox("Correct Label",
                            ALL_MZL, 
                            key=f"label_{i}", 
                            index=st.session_state.zip_detect[i][1][0] - 1,
                            label_visibility='hidden',
                            on_change=fct.update_zip_detect,
                            args=(i,))
            rowImgDet.button("🗑️", key=f"delete_{i}",
                             on_click=fct.del_unknow_glyphs, args=(i,))
    else:
        fct.space()

        cols_correct = st.columns(3)
        with cols_correct[1]:
            st.subheader("No glyphs to correct")

## - Summary before saving
else:
    fct.space()

    cols = st.columns(2)
    with cols[0]:
        _cCL, colCC, _cCR = st.columns([1,2,1])
        colCC.subheader("Corrected Glyphs")
        fct.space()

        rowCorrectGlyph = row([0.3, 0.7], gap='small')
        for i, result in enumerate(st.session_state.correct_label):
            rowCorrectGlyph.image(result[0])
            rowCorrectGlyph.write(f"""
            <p style='padding-top: 24px;
                    font-size: 20px;'>
            <b>
                {result[1][0]}
                <span style='margin-left: 16px;'>&nbsp;</span>
                {result[1][1]} - {result[1][2]}
            <span style='margin-left: 24px;'>&nbsp;</span>
            <em style='font-size: 16px;'>
                (corrected)
            </em>
            </b>
            </p>
            """, unsafe_allow_html=True)

    with cols[1]:
        _cPL, colPC, _cPR = st.columns([1,2,1])
        colPC.subheader("Predicted Glyphs")
        fct.space()

        rowPredictedGlyph = row([0.3, 0.7], gap='small')
        for i, result in enumerate(st.session_state.zip_detect):
            rowPredictedGlyph.image(result[0])
            rowPredictedGlyph.write(f"""
                <p style='padding-top: 24px;
                        font-size: 20px;'>
                <b>
                    {result[1][0]}
                    <span style='margin-left: 16px;'>&nbsp;</span>
                    {result[1][1]} - {result[1][2]}
                </b>
                <span style='margin-left: 24px;'>&nbsp;</span>
                <em style='font-size: 16px;'>
                    ({result[1][3]}%)
                </em>
                </p>
                """, unsafe_allow_html=True)

if save_button:
    st.switch_page("pages/save_result.py")
