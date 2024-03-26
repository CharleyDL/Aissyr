#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================


import bcrypt
import streamlit as st
import streamlit_authenticator as sa
import utils.functions as fct


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR', 
                   page_icon='asset/fav32.png', 
                   layout='centered')


## ---------------------------- MAIN CONTENT -------------------------------- ##

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.header("Create New Account")

    with st.form("register"):
        colH1,colH2,colH3 = st.columns([1, 1, 1])
        with colH2:
            fct.space()
            st.image('asset/logo_aissyr_M.png')

        colM1, colM2, colM3 = st.columns([1, 2, 2])
        with colM1:
            title = st.selectbox(
                "Title",
                ( "M", "Mme", "Mx", "Dr", "Dre", "Drx", "Pr", "Pre", "Prx"),
                label_visibility='hidden', index=None,
                placeholder='-', key='title'
            )

        with colM2:
            first_name = st.text_input(
                "First Name", placeholder=f"First Name",
                label_visibility='hidden', key='first_name'
            )

        with colM3:
            last_name = st.text_input(
                "Last Name", placeholder="Last Name",
                label_visibility='hidden', key='last_name'
            )

        email = st.text_input(
            "email", placeholder="email",
            label_visibility='hidden', key='email'
        )

        password = st.text_input(
            "password", placeholder="password",
            label_visibility='hidden', type='password', key='password'
        )


        colF1,colF2,colF3 = st.columns([1, 1, 1])

        with colF2:
            fct.space()
            if st.form_submit_button("Create account"):
                hash_password = fct.hash_bcrypt(password)
                credentials = [title, first_name, last_name, email, hash_password]

                res = fct.postgres_execute_insert_new_user(credentials)
                if res:
                    st.switch_page("pages/login.py")
                else:
                    st.toast("Account creation failed. Email already exists.",
                             icon='🚫')
