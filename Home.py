#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import json
import os
import requests
import streamlit as st
import streamlit_antd_components as sac

import utils.functions as fct


API_URL = os.getenv("API_URL")


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR', 
                   page_icon='asset/fav32.png', 
                   layout='wide')


## ---------------------------- LANDING PAGE -------------------------------- ##

left_column, right_column = st.columns(2)

## - Left Column
with left_column:
    for i in range(8):
        fct.space()
    # st.image('asset/logo_aissyr_L.png')
    st.image('asset/logo_landing.png')

## - Right Column
with right_column:
    for i in range(4):
        fct.space()

    st.write("""
        <h2><b style='color: #DEA15B;'>EMPOWER</b> ASSYRIAN CUNEIFORM RESEARCH 
            WITH YOUR <b style='color: #DEA15B;'>NEW AI TOOLKIT COMPANION</b>
        </h2>
        """, unsafe_allow_html=True
    )

    st.markdown('-----')
    for i in range(3):
        fct.space()

    colM1,colM2,colM3 = st.columns([1, 3, 1])
    with colM2:
        with st.form("login", border=False):
            user_email = st.text_input("email", placeholder="email",
                label_visibility='hidden', key="email",
            )

            user_pwd = st.text_input("password", placeholder="password",
                label_visibility='hidden', type='password', key="password",
            )

            if st.form_submit_button("Log In"):
                credentials = {
                    "email": user_email,
                    "input_pwd": user_pwd
                }

                res = requests.post(url=f"{API_URL}/account/verify_login/", 
                                    data=json.dumps(credentials))

                response_data = res.json()
                if response_data['result']:
                    if 'f_name' not in st.session_state:
                        st.session_state.f_name = response_data['content']['first_name']
                    if 'log' not in st.session_state:
                        st.session_state['log'] = False
                    st.switch_page("pages/main_page.py")
                else:
                    st.toast(f"{response_data['message']}", icon='🚫')

        fct.space()
        st.page_link('pages/register.py', label="Not an account yet? Sign Up")


## ------------------------------- FOOTER ----------------------------------- ##

    for i in range(8):
        fct.space()

    f1, f2, f3 = st.columns(3)

    with f3:
        sac.buttons([
            sac.ButtonsItem(label='LinkedIn', icon='linkedin', 
                            href='https://www.linkedin.com/in/charleylebarbier/'),
            sac.ButtonsItem(label='Github', icon='github', 
                            href='https://github.com/CharleyDL'),
        ], align='center')

        st.write(
            """
            <h6 style='padding-left: 92px;'>©2024 - Charley ∆.L.</h6>
            """, unsafe_allow_html=True
        )


## ---------------------------- SESSION STATE ------------------------------- ##

if "correct_label" not in st.session_state:
    st.session_state.correct_label = []

if "disabled_detect" not in st.session_state:
    st.session_state.disabled_detect = True

if "disable_btns_correct_page" not in st.session_state:
    st.session_state.disable_btns_correct_page = True

if "disable_btns_detect_page" not in st.session_state:
    st.session_state.disable_btns_detect_page = True

if 'preview_imgs' not in st.session_state:
    st.session_state.preview_imgs = []

if 'rects_annotation' not in st.session_state:
    st.session_state.rects_annotation = []

if 'rects_correct' not in st.session_state:
    st.session_state.rects_correct = []

if 'rects_detect' not in st.session_state:
    st.session_state.rects_detect = []

if "upload_file" not in st.session_state:
    st.session_state.upload_file = None

if 'zip_detect' not in st.session_state:
    st.session_state.zip_detect = []
