#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Thursday 2 May 2024
# ==============================================================================

import os
import sys

from fastapi.testclient import TestClient

## Add the current directory to the path
sys.path.append(".")
from api import app


class TestAPIResources:

    client = TestClient(app)
    API_URL = os.getenv("API_URL")

    def test_all_glyphs(self):
        response = self.client.get(url=f"{self.API_URL}/resources/glyphs/")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert len(response.json()) > 0 and len(response.json()) <= 907


    def test_glyph_by_mzl(self):
        mzl_number = 13
        expected_response = {
            "mzl_number": 13,
            "glyph_name": "MUG@g",
            "glyph": "𒈯",
            "glyph_phonetic": [
                "uttu₄",
                "uṭu₄",
                "zadim"
            ]
        }

        response = self.client.get(url=f"{self.API_URL}/resources/glyphs/{mzl_number}/")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json() == expected_response
