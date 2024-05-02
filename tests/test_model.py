#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import os


class TestLoadModel:

    def test_get_envvar(self):
        print("Valeur de 'API_URL' dans l'environnement:", os.getenv('API_URL'))
        print("Valeur de 'DAGSHUB_REPO_OWNER' dans l'environnement:", os.getenv('DAGSHUB_REPO_OWNER'))
        print("Valeur de 'DAGSHUB_REPO' dans l'environnement:", os.getenv('DAGSHUB_REPO'))
        print("Valeur de 'MODEL_URI' dans l'environnement:", os.getenv('MODEL_URI'))

        assert os.getenv('API_URL') is not None
        assert os.getenv('DAGSHUB_REPO_OWNER') is not None
        assert os.getenv('DAGSHUB_REPO') is not None
        assert os.getenv('MODEL_URI') is not None


#     def test_load_model(self):
#         model = load_model()
#         assert model is not None
#         assert hasattr(model, "predict")