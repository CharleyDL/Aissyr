#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import streamlit as st
import streamlit_antd_components as sac

import utils.functions as fct


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR', 
                   page_icon='asset/fav32.png', 
                   layout='wide')

if fct.check_session():
    st.toast("Authentication successful", icon='🎉')


## -------------------------------- LOGO ------------------------------------ ##

h_left, h_center,h_right = st.columns(3)

with h_center:
    st.markdown(
    """
    <style>
        [data-testid=stImage]{ margin-left: 48px; }
    </style>
    """, unsafe_allow_html=True
    )
    st.image('asset/logo_aissyr_L.png')


for i in range(3):
    fct.space()

st.header(f'Welcome {st.session_state["f_name"]}!')
st.markdown('----')


## ---------------------------- MAIN CONTENT -------------------------------- ##

r1_c1, r1_c2 = st.columns([1, 2])
with r1_c1:
    st.subheader('Methodology')
    st.write(
        """
        <div style='margin-left: 24px; margin-right: 80px;'>
            <b>AIssyr Web App is dedicated to CNRS researchers to work on the 
            Neo-Assyrian cuneiforms writing system, providing a toolbox for 
            detecting and annotating images.</b>
        </div>
        <br />
        <div style='margin-left: 24px; margin-right: 80px;'>
            This streamlit web app is a prototype to demonstrate the different 
            features before implement the web-app <i><b>(Django)</b></i> with a 
            friendly interface.
        </div>
        <br />
        <div style='margin-left: 24px; margin-right: 80px;'>
            Currently, <i><b>glyphs are detected using a bounding box drawn by 
            the user.</b></i> In the future, this will be replaced by automatic 
            glyph detection <i><b>(october 2024)</b></i>
        </div>
        """, unsafe_allow_html=True
    )

with r1_c2:
    r2_c1, r2_c2 = st.columns(2)

    with r2_c1: 
        st.subheader('Features')
        st.write(
            """
            <div>
                <li style='list-style-type:none;'>----- <b>Login</b> and 
                    <b>Sign up</b></li>
                <li style='list-style-type:none;'>----- <b>Detection from an 
                    image</b> with a <b>manual bounding box</b></li>
                <li style='list-style-type:none;'>----- <b>Annotation to label 
                    glyphs</b></li>
                <li style='list-style-type:none;'>----- <b>Archive 
                    consultation</b></li>
            </div>
            """, unsafe_allow_html=True
        )

    with r2_c2:
        st.subheader('Schedule -- possible changes')
        st.write(
            """
            <div>
                <li style='list-style-type:none;'>----- Streamlit with Manual 
                    Detection : <i><b>May 2024</i></b></li>
                <li style='list-style-type:none;'>----- Django version : 
                    <i><b>July 2024</i></b></li>
                <li style='list-style-type:none;'>----- Automatic Detection : 
                    <i><b>October 2024</i></b></li>
                <li style='list-style-type:none;'>----- Text Translation 
                    : <i><b>March/April 2025</i></b></li>
                <li style='list-style-type:none;'>----- Image classification by 
                    theme : <i><b>May 2025</i></b></li>
            </div>
            """, unsafe_allow_html=True
        )


## ------------------------------ SIDEBAR ----------------------------------- ##

with st.sidebar:
    st.write("""
             <h3 style='text-align: center;'>🧰 TOOLKIT</h3>
             """, unsafe_allow_html=True)

    for i in range(3):
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

    for i in range(36):
        fct.space()

    cols = st.columns([1,1,1])

    with cols[1]:
        logout_button = st.button("Logout")
        if logout_button:
            fct.logout()


## ------------------------------- FOOTER ----------------------------------- ##

st.markdown('----')

f_left, f_left_cent, f_center, f_right_cent, f_right = st.columns([2, 1, 1,
                                                                   1, 2])
with f_left:
    st.write(
        """
        <h6 style='padding-left: 92px;'>©2024 - Charley ∆.L.</h6>
        """, unsafe_allow_html=True
    )

with f_right:
    sac.buttons([
        sac.ButtonsItem(label='LinkedIn', icon='linkedin',
                        href='https://www.linkedin.com/in/charleylebarbier/'),
        sac.ButtonsItem(label='Github', icon='github',
                        href='https://github.com/CharleyDL'),
    ], align='center')
