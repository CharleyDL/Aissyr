#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 30 Apr. 2024
# ==============================================================================
# Test to check if required elements are present in the project.
# ==============================================================================

import os
import unittest




class TestRequiredElements(unittest.TestCase):

    def test_folder_exists(self):
        required_folders = ['routers', 'utils'] 
        for folder in required_folders:
            assert os.path.exists(folder)

    def test_file_exists(self):
        required_files = ['api.py', 'Procfile', 'requirements.txt', 'runtime.txt',
                          'routers/account.py', 'routers/archives.py', 
                          'routers/labelisation.py', 'routers/prediction.py', 
                          'routers/resources.py', 
                          'utils/database.py', 'utils/functions.py', 
                          'utils/schemas.py']
        for file in required_files:
            assert os.path.exists(file)
