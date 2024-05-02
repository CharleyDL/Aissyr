#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import dagshub
import mlflow.pyfunc
import os

from dotenv import load_dotenv


load_dotenv()


class TestLoadModel:

    def test_load_model(self):
        DAGSHUB_REPO = os.getenv('DAGSHUB_REPO')
        DAGSHUB_REPO_OWNER = os.getenv('DAGSHUB_REPO_OWNER')
        DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN')
        MODEL_URI = os.getenv('MODEL_URI')

        dagshub.auth.add_app_token(token=DAGSHUB_USER_TOKEN)
        dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER, mlflow=True)

        model = mlflow.pyfunc.load_model(MODEL_URI)
        assert model is not None
