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

import utils.functions as fct


API_URL = os.getenv("API_URL")


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR', 
                   page_icon='asset/fav32.png', 
                   layout='centered'
                   )


## ----------------------------- LOG IN FORM -------------------------------- ##

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.header("Sign In")

    with st.form("login"):
        colH1,colH2,colH3 = st.columns([1, 1, 1])
        with colH2:
            fct.space()
            st.image('asset/logo_aissyr_M.png')

        user_email = st.text_input("email", placeholder="email",
            label_visibility='hidden', key="email",
        )

        user_pwd = st.text_input("password", placeholder="password",
            label_visibility='hidden', type='password', key="password",
        )

        colF1,colF2,colF3 = st.columns([2, 1, 2])

        with colF2:
            fct.space()
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
