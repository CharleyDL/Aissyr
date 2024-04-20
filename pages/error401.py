#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 20 Apr. 2024
# ==============================================================================


import streamlit as st
import streamlit_antd_components as sac
import utils.functions as fct


## ----------------------------- SETUP PAGE --------------------------------- ##

st.set_page_config(page_title='AISSYR', 
                   page_icon='asset/fav32.png', 
                   layout='wide')

## ---------------------------- ERROR 401 PAGE ------------------------------ ##


## - SHIEL ICON
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
st.image('asset/icn_shield.png')


## - ERROR MESSAGE
st.write("""
    <h2 style='text-align: center;'>
        ERROR 401 - NOT AUTHORIZED, PLEASE LOGIN
    </h2>
        """, unsafe_allow_html=True)

for i in range(3):
    fct.space()


## - LOGIN BUTTON
st.markdown("""
    <style>
    [data-testid="baseButton-secondary"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

login_button = st.button("log In")
if login_button:
    fct.logout()