#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 20 Apr. 2024
# ==============================================================================

import os

from dotenv import load_dotenv


load_dotenv()


class TestRequiredElements:

    def test_folder_exists(self):
        required_folders = ['.streamlit', 'asset', 'pages', 
                            'streamlit_img_label', 'utils']
        for folder in required_folders:
            assert os.path.exists(folder)

    def test_file_exists(self):
        required_files = ['asset/icn_save.png', 'asset/icn_shield.png',
                          'asset/logo_landing.png', 'asset/logo_aissyr_S.png', 
                          'asset/logo_aissyr_M.png', 'asset/logo_aissyr_L.png', 
                          'pages/labelisation_page.py', 'pages/archive.py',
                          'pages/correct_label.py', 'pages/detect_page.py',
                          'pages/error401.py', 'pages/login.py', 
                          'pages/main_page.py', 'pages/register.py',
                          'pages/save_result.py', 'pages/select_label.py',
                          'utils/functions.py',
                          'Home.py', 'requirements.txt', 
                          '.streamlit/config.toml',
                         ]

        for file in required_files:
            assert os.path.exists(file)


class TestEnvVar:

    def test_get_envvar(self):
        assert os.environ['API_URL'] is not None, "API_URL is not defined"
        assert os.environ['DAGSHUB_REPO_OWNER'] is not None, "DAGSHUB_REPO_OWNER is not defined"
        assert os.environ['DAGSHUB_REPO'] is not None, "DAGSHUB_REPO is not defined"
        assert os.environ['DAGSHUB_USER_TOKEN'] is not None, "DAGSHUB_USER_TOKEN is not defined"
        assert os.environ['MODEL_URI'] is not None, "MODEL_URI is not defined"
