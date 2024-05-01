#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 20 Apr. 2024
# ==============================================================================

import streamlit as st

from streamlit_extras.row import row
from streamlit_img_label.manage import ImageManager

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


## ------------------------------ SUCCESS PAGE ------------------------------ ##

## - SUCCESS ICON
st.markdown(
"""
<style>
    [data-testid=stImage]{ 
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True
)
st.image('asset/icn_save.png')


## - SUCCES MESSAGE
st.write("""
    <h2 style='text-align: center;'>
        DATABASE BACKUP SUMMARY
    </h2>
        """, unsafe_allow_html=True)

st.markdown('----')

for i in range(3):
    fct.space()


## - SUMMARY OF CORRECTED AND PREDICTED GLYPHS
st.write("""
    <h4 style='text-align: center;'>
        Summary
    </h4>
        """, unsafe_allow_html=True)

rowImgDet = row([0.3, 0.7], gap='small')

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


## --------------------------- SAVING IN DATABASE --------------------------- ##

# - Check if the user is in DEMO mode
if st.session_state.f_name == 'DEMO':
    st.toast(f"""This is a demo version, 
             the data is not saved in the database.""", icon='🚫')
else:
    ## -- Prepare the image info
    img = ImageManager(st.session_state.upload_file).get_img()
    img_name = st.session_state.upload_file.name

    width, height = img.size
    bbox_img = [0, 0, width, height]    # Need for the annotation save not inference


    ## -- Send Corrected Glyphs to the API and display the message
    label_results = fct.save_labelisation(img_name,
                        img,
                        bbox_img,
                        st.session_state.rects_correct,
                        st.session_state.correct_label)

    for i, result in enumerate(label_results):
        if result['result']:
                st.toast(result['message'], icon='✅')
        else:
            st.toast(result['message'], icon='🚫')


    ## -- Send Predicted Glyphs to the API and display the message
    pred_results = fct.save_inference(img_name,
                                    img,
                                    st.session_state.rects_detect,
                                    st.session_state.zip_detect)

    for i, result in enumerate(pred_results):
        if result['result']:
                st.toast(result['message'], icon='✅')
        else:
            st.toast(result['message'], icon='🚫')


## ------------------------------ SESSION STATE ----------------------------- ##

fct.disable_btns_correct_page()            # - Reset the correct page buttons
