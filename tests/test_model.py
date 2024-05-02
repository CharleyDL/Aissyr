#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import os

# from utils.functions import load_model


class TestLoadModel:

    def test_get_envvar(self):
        assert os.environ.get("DAGSHUB_REPO_OWNER") is not None
        assert os.environ.get("DAGSHUB_REPO") is not None
        assert os.environ.get("MODEL_URI") is not None

#     def test_load_model(self):
#         model = load_model()
#         assert model is not None
#         assert hasattr(model, "predict")