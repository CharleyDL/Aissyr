#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import os

# from utils.functions import load_model


API_URL = os.environ("API_URL",)
DAGSHUB_REPO_OWNER = os.environ("DAGSHUB_REPO_OWNER")
DAGSHUB_REPO = os.environ("DAGSHUB_REPO")
MODEL_URI = os.environ("MODEL_URI")



class TestLoadModel:

    def test_get_envvar(self):
        envvar = [API_URL, DAGSHUB_REPO_OWNER, DAGSHUB_REPO, MODEL_URI]

        for var in envvar:
            assert var in os.environ, f"{var} is not in os.environ"



#     def test_load_model(self):
#         model = load_model()
#         assert model is not None
#         assert hasattr(model, "predict")