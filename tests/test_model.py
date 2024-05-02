#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import os

from dotenv import load_dotenv


load_dotenv()


class TestEnvVar:

    def test_get_envvar(self):
        api_url = os.getenv('API_URL')
        dagshub_repo_owner = os.getenv('DAGSHUB_REPO_OWNER')
        dagshub_repo = os.getenv('DAGSHUB_REPO')
        model_uri = os.getenv('MODEL_URI')

        print(f"API URL: {api_url}")
        print(f"Dagshub Repo Owner: {dagshub_repo_owner}")
        print(f"Dagshub Repo: {dagshub_repo}")
        print(f"Model URI: {model_uri}")

        assert api_url is not None
        assert dagshub_repo_owner is not None
        assert dagshub_repo is not None
        assert model_uri is not None




# class TestLoadModel:
    
#     def test_load_model(self):
#         model = load_model()
#         assert model is not None
#         assert hasattr(model, "predict")